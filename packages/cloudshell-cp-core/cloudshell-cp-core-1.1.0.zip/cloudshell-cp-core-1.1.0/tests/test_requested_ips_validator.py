import unittest

from mock import Mock, patch

from cloudshell.cp.core.requested_ips.validator import RequestedIPsValidator


class TestRequestedIPsValidator(unittest.TestCase):

    def test_validate_ip_address_passes(self):
        # arrange
        ip = '10.0.0.1'

        # act
        RequestedIPsValidator.validate_ip_address(ip)

    def test_validate_ip_address_failes(self):
        # arrange
        ip = '10.0.0.350'

        # act & assert
        with self.assertRaises(ValueError):
            RequestedIPsValidator.validate_ip_address(ip)

    @patch('cloudshell.cp.core.requested_ips.validator.RequestedIPsValidator.validate_ip_address_range_basic')
    def test_is_range_true(self, validate_ip_address_range_mock):
        # arrange
        ip = Mock()

        # act
        result = RequestedIPsValidator.is_range(ip)

        # assert
        self.assertTrue(result)

    @patch('cloudshell.cp.core.requested_ips.validator.RequestedIPsValidator.validate_ip_address_range_basic')
    def test_is_range_false(self, validate_ip_address_range_mock):
        # arrange
        ip = Mock()
        validate_ip_address_range_mock.side_effect = ValueError

        # act
        result = RequestedIPsValidator.is_range(ip)

        # assert
        self.assertFalse(result)

    def test_validate_ip_address_range_passes(self):
        # arrange
        range = '10.0.0.1-10'

        # act
        RequestedIPsValidator.validate_ip_address_range_basic(range)

    def test_validate_ip_address_range_error_basic_structure(self):
        # arrange
        range = '10.0.0.1'  # no '-' to specify range

        # act & assert
        with self.assertRaisesRegexp(ValueError, 'Missing delimiter'):
            RequestedIPsValidator.validate_ip_address_range_basic(range)

    def test_validate_ip_address_range_error_ip_address_invalid(self):
        # arrange
        range = 'xxx-20'  # no '-' to specify range

        # act & assert
        with self.assertRaises(ValueError):
            RequestedIPsValidator.validate_ip_address_range_basic(range)

    def test_validate_ip_address_range_error_range_length_not_int(self):
        # arrange
        range = '10.0.0.1-xx'  # range length must be integer

        # act & assert
        with self.assertRaisesRegexp(ValueError, 'range length is not a valid integer'):
            RequestedIPsValidator.validate_ip_address_range_basic(range)
