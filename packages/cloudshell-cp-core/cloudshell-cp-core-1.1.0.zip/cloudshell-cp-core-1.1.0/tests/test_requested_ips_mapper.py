import unittest

from mock import Mock, MagicMock

from cloudshell.cp.core.requested_ips.mapper import RequestedIPsMapper


class TestRequestedIPsMapper(unittest.TestCase):

    def test_map_network_to_requested_ips_successfully(self):
        # arrange
        requested_ips_for_subnet1 = ['10.0.0.5', '10.0.0.8']
        requested_ips_for_subnet2 = ['10.0.0.20', '10.0.0.21', '10.0.0.22']
        requested_ips_list = [requested_ips_for_subnet1, requested_ips_for_subnet2]
        mapper = RequestedIPsMapper(requested_ips_list)

        action1 = Mock()
        cidr1 = '10.0.0.0/28'
        action1.actionParams.cidr = cidr1
        action2 = Mock()
        cidr2 = '10.0.0.16/28'
        action2.actionParams.cidr = cidr2
        network_actions = [action1, action2]

        # act
        result = mapper.map_network_to_requested_ips(network_actions)

        # assert
        self.assertTrue(cidr1 in result)
        self.assertTrue(cidr2 in result)
        self.assertListEqual(requested_ips_for_subnet1, result.get(cidr1))
        self.assertListEqual(requested_ips_for_subnet2, result.get(cidr2))

    def test_map_network_to_requested_ips_error_req_ip_out_of_range(self):
        # arrange
        requested_ips_for_subnet1 = ['10.0.0.5', '10.0.0.18']
        requested_ips_for_subnet2 = ['10.0.0.20', '10.0.0.21', '10.0.0.22']
        requested_ips_list = [requested_ips_for_subnet1, requested_ips_for_subnet2]
        mapper = RequestedIPsMapper(requested_ips_list)

        action1 = Mock()
        cidr1 = '10.0.0.0/28'
        action1.actionParams.cidr = cidr1
        action2 = Mock()
        cidr2 = '10.0.0.16/28'
        action2.actionParams.cidr = cidr2
        network_actions = [action1, action2]

        # act & assert
        with self.assertRaisesRegexp(ValueError, 'outside of network 10.0.0.0/28'):
            mapper.map_network_to_requested_ips(network_actions)

    def test__map_network_to_requested_ips_empty_requested_ips(self):
        # arrange
        requested_ips_list = None
        network_actions = MagicMock()
        mapper = RequestedIPsMapper(requested_ips_list)

        # act
        result = mapper.map_network_to_requested_ips(network_actions)

        # assert
        self.assertEqual(result, {})
