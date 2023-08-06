from __future__ import (absolute_import, division, print_function, unicode_literals)
from builtins import str

import ipaddress


class RequestedIPsMapper:

    def __init__(self, requested_ips_list):
        """
        :param List[List[str]] requested_ips_list:
        """
        self._requested_ips_list = requested_ips_list

    def map_network_to_requested_ips(self, network_actions):
        """
        :param List[cloudshell.cp.core.models.ConnectSubnet] network_actions:
        :rtype: Dict[str, List[str]]
        """
        if not self._requested_ips_list:
            return {}

        cidrs = list(map(lambda x: x.actionParams.cidr, network_actions))
        requested_ips_list_address_obj = \
            list(map(lambda ips_for_nic:
                (list(map(lambda x: ipaddress.ip_address(str(x)), ips_for_nic)), ips_for_nic),
                self._requested_ips_list))

        cidrs_to_req_ips = {}

        for subnet_cidr in cidrs:
            subnet = ipaddress.ip_network(str(subnet_cidr))

            for ips_for_nic_ipaddress_obj, ips_for_nic in requested_ips_list_address_obj:
                # check if all ips are in subnet
                if all(ip in subnet for ip in ips_for_nic_ipaddress_obj):
                    cidrs_to_req_ips[subnet_cidr] = ips_for_nic
                    continue

                # check if any ip is in subnet -> if true it means some IPs are outside of subnet range
                # so need to raise error
                if any(ip in subnet for ip in ips_for_nic_ipaddress_obj):
                    raise ValueError('Some of the requested IPs are outside of network {}'.format(subnet_cidr))

        return cidrs_to_req_ips