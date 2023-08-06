from __future__ import (absolute_import, division, print_function, unicode_literals)
from builtins import str

import ipaddress

from cloudshell.cp.core.requested_ips.validator import RequestedIPsValidator

PRIVATE_IP_ATTR = 'Private IP'


class RequestedIPsParser:

    @staticmethod
    def parse(attributes):
        """
        Look for 'Private IP' attribute and parse it
        :param dict attributes:
        :rtype: list
        :return: List[List[str]] - Each item in the list represents the IP addresses per specific nic.
        """
        ips_request_string = RequestedIPsParser._get_private_ip_attribute_value(attributes)
        if not ips_request_string or not ips_request_string.strip():
            return None

        requested_ips = []

        for ip_req_for_nic in ips_request_string.split(';'):
            requested_ips_for_nic = []
            for ip_req_single in ip_req_for_nic.split(','):
                ip_req_single = ip_req_single.strip()
                if RequestedIPsValidator.is_range(ip_req_single):
                    ip_in_range = RequestedIPsParser._parse_range(ip_req_single)
                    requested_ips_for_nic.extend(ip_in_range)

                else:
                    RequestedIPsValidator.validate_ip_address(ip_req_single)
                    requested_ips_for_nic.append(ip_req_single)

            requested_ips.append(requested_ips_for_nic)

        return requested_ips

    @staticmethod
    def _get_private_ip_attribute_value(attributes):
        """
        :param dict attributes:
        :rtype: str
        """
        ips_request = None

        if PRIVATE_IP_ATTR in attributes:
            ips_request = attributes[PRIVATE_IP_ATTR]

        else:
            # try to get attribute using 2nd gen shell formatting
            private_ip_attr_2nd_gen = '.' + PRIVATE_IP_ATTR
            for attribute_name in attributes.keys():
                if attribute_name.endswith(private_ip_attr_2nd_gen):
                    ips_request = attributes[attribute_name]
                    break

        return ips_request

    @staticmethod
    def _parse_range(ip_req_single):
        """
        :param str ip_req_single:
        :rtype: list
        """
        range_start, range_length = ip_req_single.split('-')
        start_ip = ipaddress.ip_address(str(range_start))

        ips_in_range = []
        for i in range(0, int(range_length) + 1):
            ips_in_range.append(str(start_ip + i))

        return ips_in_range


