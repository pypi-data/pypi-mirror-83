import unittest

from mock import MagicMock

from cloudshell.cp.core.requested_ips.parser import RequestedIPsParser


class TestRequestedIPsParser(unittest.TestCase):

    def test_parser_single_ip(self):
        # arrange
        attributes = {'Private IP': '10.0.0.1'}

        # act
        result = RequestedIPsParser.parse(attributes)

        # assert
        self.assertListEqual(result, [['10.0.0.1']])

    def test_parser_single_range(self):
        # arrange
        attributes = {'Private IP': '10.0.0.10-4'}

        # act
        result = RequestedIPsParser.parse(attributes)

        # assert
        self.assertListEqual(result, [['10.0.0.10', '10.0.0.11', '10.0.0.12', '10.0.0.13', '10.0.0.14']])

    def test_parser_multiple_ips_single_nic(self):
        # arrange
        attributes = {'Private IP': '10.0.0.1,10.0.0.5,10.0.0.7'}

        # act
        result = RequestedIPsParser.parse(attributes)

        # assert
        self.assertListEqual(result, [['10.0.0.1', '10.0.0.5', '10.0.0.7']])

    def test_parser_multiple_ips_and_multiple_ranges_single_nic(self):
        # arrange
        attributes = {'Private IP': '10.0.0.1,10.0.0.5,10.0.0.7-3,10.0.0.20-2'}

        # act
        result = RequestedIPsParser.parse(attributes)

        # assert
        self.assertListEqual(result, [['10.0.0.1', '10.0.0.5', '10.0.0.7', '10.0.0.8', '10.0.0.9', '10.0.0.10',
                                       '10.0.0.20', '10.0.0.21', '10.0.0.22']])

    def test_parser_single_ip_multiple_nics(self):
        # arrange
        attributes = {'Private IP': '10.0.0.1;10.0.0.100;10.0.0.200'}

        # act
        result = RequestedIPsParser.parse(attributes)

        # assert
        self.assertListEqual(result, [['10.0.0.1'], ['10.0.0.100'], ['10.0.0.200']])

    def test_parser_multiple_ips_and_multiple_ranges__for_multiple_nics(self):
        # arrange
        attributes = {'Private IP': '10.0.0.1,10.0.0.3,10.0.0.10-2;10.0.0.100-4;10.0.0.200-2,10.0.0.210'}

        # act
        result = RequestedIPsParser.parse(attributes)

        # assert
        self.assertListEqual(result, [['10.0.0.1', '10.0.0.3', '10.0.0.10', '10.0.0.11', '10.0.0.12'],
                                      ['10.0.0.100', '10.0.0.101', '10.0.0.102', '10.0.0.103', '10.0.0.104'],
                                      ['10.0.0.200', '10.0.0.201', '10.0.0.202', '10.0.0.210']])

    def test_parser_with_spaces_between_delimiter(self):
        # arrange
        attributes = {'Private IP': '10.0.0.1, 10.0.0.10-2; 10.0.0.100-4 ; 10.0.0.200 , 10.0.0.210 ,10.0.0.214'}

        # act
        result = RequestedIPsParser.parse(attributes)

        # assert
        self.assertListEqual(result, [['10.0.0.1', '10.0.0.10', '10.0.0.11', '10.0.0.12'],
                                      ['10.0.0.100', '10.0.0.101', '10.0.0.102', '10.0.0.103', '10.0.0.104'],
                                      ['10.0.0.200', '10.0.0.210', '10.0.0.214']])

    def test_parse_throws_ip_address_not_valid(self):
        # arrange
        attributes = {'Private IP': '10.0.0.300'}  # ip address is not valid

        # act & assert
        with self.assertRaises(ValueError):
            RequestedIPsParser.parse(attributes)

    def test_parser_no_private_ip_attribute(self):
        # arrange
        attributes = MagicMock()

        # act
        result = RequestedIPsParser.parse(attributes)

        # assert
        self.assertIsNone(result)

    def test_parser_empty_private_ip_attribute(self):
        # arrange
        attributes = {'Private IP': ''}

        # act
        result = RequestedIPsParser.parse(attributes)

        # assert
        self.assertIsNone(result)

    def test_parser_empty_private_ip_attribute_with_spaces(self):
        # arrange
        attributes = {'Private IP': '    '}

        # act
        result = RequestedIPsParser.parse(attributes)

        # assert
        self.assertIsNone(result)
