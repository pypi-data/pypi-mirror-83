from unittest import TestCase

from cloudshell.cp.core import DriverRequestParser
from cloudshell.cp.core.models import *
from cloudshell.cp.core.utils import *
import json


class TestCloudShellCpCore(TestCase):

    def test_custom_deployment_model(self):
        # prepare
        class CustomModel(object):
            __deploymentModel__ = "VCenter Deploy VM From Linked Clone"

            def __init__(self, attributes):
                self.auto_power_off = attributes['Auto Power Off']
                self.autoload = attributes['Autoload']

        atts_json = '[{"attributeName":"Auto Delete","attributeValue":"True","type":"attributes"},{"attributeName":"Autoload","attributeValue":"True","type":"attributes"},{"attributeName":"IP Regex","attributeValue":"","type":"attributes"},{"attributeName":"Refresh IP Timeout","attributeValue":"600","type":"attributes"},{"attributeName":"vCenter VM","attributeValue":"Tor/Temps/ImageMonoNew","type":"attributes"},{"attributeName":"vCenter VM Snapshot","attributeValue":"1","type":"attributes"},{"attributeName":"VM Cluster","attributeValue":"","type":"attributes"},{"attributeName":"VM Storage","attributeValue":"","type":"attributes"},{"attributeName":"VM Resource Pool","attributeValue":"","type":"attributes"},{"attributeName":"VM Location","attributeValue":"","type":"attributes"},{"attributeName":"Auto Power On","attributeValue":"True","type":"attributes"},{"attributeName":"Auto Power Off","attributeValue":"True","type":"attributes"},{"attributeName":"Wait for IP","attributeValue":"True","type":"attributes"}]'
        deploy_req_json = '{"driverRequest":{"actions":[{"actionParams":{"appName":"vCenter_CVC_Support","deployment":{"deploymentPath":"VCenter Deploy VM From Linked Clone","attributes": ' + atts_json + ' ,"type":"deployAppDeploymentInfo"},"appResource":{"attributes":[{"attributeName":"Password","attributeValue":"3M3u7nkDzxWb0aJ/IZYeWw==","type":"attributes"},{"attributeName":"Public IP","attributeValue":"","type":"attributes"},{"attributeName":"User","attributeValue":"","type":"attributes"}],"type":"appResourceInfo"},"type":"deployAppParams"},"actionId":"7808cf76-b8c5-4392-b571-5da99836b84b","type":"deployApp"}]}}'

        # act
        parser = DriverRequestParser()
        parser.add_deployment_model(CustomModel)

        action = parser.convert_driver_request_to_actions(deploy_req_json)[0]

        # assert
        self.assertTrue(action.actionParams.deployment.customModel.autoload, 'True')
        self.assertTrue(action.actionParams.deployment.customModel.auto_power_off, 'True')

    def test_custom_deployment_model_slicker(self):
        # prepare
        class CustomModel(object):
            __deploymentModel__ = "VCenter Deploy VM From Linked Clone"

            def __init__(self, attributes):
                self.auto_power_off = False
                self.autoload = ''

                for k, v in attributes.items():
                    try_set_attr(self, to_snake_case(k), v)

        atts_json = '[{"attributeName":"Auto Delete","attributeValue":"True","type":"attributes"},{"attributeName":"Autoload","attributeValue":"True","type":"attributes"},{"attributeName":"IP Regex","attributeValue":"","type":"attributes"},{"attributeName":"Refresh IP Timeout","attributeValue":"600","type":"attributes"},{"attributeName":"vCenter VM","attributeValue":"Tor/Temps/ImageMonoNew","type":"attributes"},{"attributeName":"vCenter VM Snapshot","attributeValue":"1","type":"attributes"},{"attributeName":"VM Cluster","attributeValue":"","type":"attributes"},{"attributeName":"VM Storage","attributeValue":"","type":"attributes"},{"attributeName":"VM Resource Pool","attributeValue":"","type":"attributes"},{"attributeName":"VM Location","attributeValue":"","type":"attributes"},{"attributeName":"Auto Power On","attributeValue":"True","type":"attributes"},{"attributeName":"Auto Power Off","attributeValue":"True","type":"attributes"},{"attributeName":"Wait for IP","attributeValue":"True","type":"attributes"}]'
        deploy_req_json = '{"driverRequest":{"actions":[{"actionParams":{"appName":"vCenter_CVC_Support","deployment":{"deploymentPath":"VCenter Deploy VM From Linked Clone","attributes": ' + atts_json + ' ,"type":"deployAppDeploymentInfo"},"appResource":{"attributes":[{"attributeName":"Password","attributeValue":"3M3u7nkDzxWb0aJ/IZYeWw==","type":"attributes"},{"attributeName":"Public IP","attributeValue":"","type":"attributes"},{"attributeName":"User","attributeValue":"","type":"attributes"}],"type":"appResourceInfo"},"type":"deployAppParams"},"actionId":"7808cf76-b8c5-4392-b571-5da99836b84b","type":"deployApp"}]}}'

        # act
        parser = DriverRequestParser()
        parser.add_deployment_model(CustomModel)

        action = parser.convert_driver_request_to_actions(deploy_req_json)[0]

        # assert
        self.assertEqual(action.actionParams.deployment.customModel.autoload, 'True')
        self.assertEqual(action.actionParams.deployment.customModel.auto_power_off, True)

    def test_deploy_app_action(self):
        # prepare
        json_req = '{"driverRequest":{"actions":[{"actionParams":{"appName":"vCenter_CVC_Support","deployment":{"deploymentPath":"VCenter Deploy VM From Linked Clone","attributes":[{"attributeName":"vCenter VM","attributeValue":"Tor/Temps/ImageMonoNew","type":"attribute"},{"attributeName":"vCenter VM Snapshot","attributeValue":"1","type":"attribute"},{"attributeName":"VM Cluster","attributeValue":"","type":"attribute"},{"attributeName":"VM Storage","attributeValue":"","type":"attribute"},{"attributeName":"VM Resource Pool","attributeValue":"","type":"attribute"},{"attributeName":"VM Location","attributeValue":"","type":"attribute"},{"attributeName":"Auto Power On","attributeValue":"True","type":"attribute"},{"attributeName":"Auto Power Off","attributeValue":"True","type":"attribute"},{"attributeName":"Wait for IP","attributeValue":"True","type":"attribute"},{"attributeName":"Auto Delete","attributeValue":"True","type":"attribute"},{"attributeName":"Autoload","attributeValue":"True","type":"attribute"},{"attributeName":"IP Regex","attributeValue":"","type":"attribute"},{"attributeName":"Refresh IP Timeout","attributeValue":"600","type":"attribute"}],"type":"deployAppDeploymentInfo"},"appResource":{"attributes":[{"attributeName":"Password","attributeValue":"3M3u7nkDzxWb0aJ/IZYeWw==","type":"attribute"},{"attributeName":"Public IP","attributeValue":"","type":"attribute"},{"attributeName":"User","attributeValue":"","type":"attribute"}],"type":"appResourceInfo"},"type":"deployAppParams"},"actionId":"ad3561c1-45a5-445a-9b5f-4021879a0b0c","type":"deployApp"}]}}'

        # act
        parser = DriverRequestParser()
        deploy_action = parser.convert_driver_request_to_actions(json_req)[0]

        # assert
        self.assertIsInstance(deploy_action, DeployApp)
        self.assertEqual(deploy_action.actionParams.appName, 'vCenter_CVC_Support')
        self.assertEqual(deploy_action.actionParams.deployment.deploymentPath, "VCenter Deploy VM From Linked Clone")
        self.assertEqual(deploy_action.actionParams.deployment.attributes["vCenter VM Snapshot"], "1")

    def test_prepare_connectivity_action(self):
        # prepare
        json_req = '{"driverRequest":{"actions":[{"actionParams":{"cidr":"10.0.1.0/24","type":"prepareCloudInfraParams"},"actionId":"36af5bbf-c9b4-4e5d-b84b-9ea513c7defd","type":"prepareCloudInfra"},{"actionParams":{"isPublic":true,"cidr":"10.0.1.0/24","alias":"DefaultSubnet","subnetServiceAttributes":null,"type":"prepareSubnetParams"},"actionTarget":{"fullName":null,"fullAddress":null,"type":"actionTarget"},"actionId":"0480fa41-f50b-42d6-9c0d-5518875f1176","type":"prepareSubnet"}]}}'
        req = json.loads(json_req)

        # act
        parser = DriverRequestParser()
        actions = parser.convert_driver_request_to_actions(req)
        self.assertEqual(len(actions), 2)
        prepare_cloud_infra = single(actions, lambda x: isinstance(x, PrepareCloudInfra))

        # assert
        self.assertEqual(prepare_cloud_infra.actionId, '36af5bbf-c9b4-4e5d-b84b-9ea513c7defd')
        self.assertEqual(prepare_cloud_infra.actionParams.cidr, '10.0.1.0/24')

        prepare_subnet = single(actions, lambda x: isinstance(x, PrepareSubnet))

        self.assertEqual(prepare_subnet.actionParams.alias, 'DefaultSubnet')
        self.assertEqual(prepare_subnet.actionParams.isPublic, True)

    def test_remove_vlan_action(self):
        # prepare

        json_req = '{  "driverRequest": {"actions": [{"connectionId":"2e85db89-f1c9-4da2-b738-6ed57d7c8ec6","connectionParams":{"vlanId":["2"],"mode":"Access","type":"setVlanParameter"},"connectorAttributes":[{"attributeName":"Interface","attributeValue":"00:50:56:a2:3c:83","type":"connectorAttribute"}],"actionId":"27409903-4d80-4607-8be2-8140285f87e6","actionTarget":{"fullName":"VM Deployment_6693d80d","fullAddress":"N/A","type":"actionTarget"},"customActionAttributes":[{"attributeName":"VM_UUID","attributeValue":"422279ec-e35a-b63f-591a-5e748514056d","type":"customAttribute"}],"type":"removeVlan"}]  }}'
        req = json.loads(json_req)

        parser = DriverRequestParser()

        # act
        action = parser.convert_driver_request_to_actions(req)[0]

        # assert
        self.assertIsInstance(action, RemoveVlan)
        self.assertEqual(action.connectionId, "2e85db89-f1c9-4da2-b738-6ed57d7c8ec6")
        self.assertEqual(action.actionId, "27409903-4d80-4607-8be2-8140285f87e6")

    def test_set_vlan_action(self):
        # prepare

        json_req = '{"driverRequest":{"actions":[{"connectionId":"3241eb47-3d9a-4dda-becf-b6c010b8622e","connectionParams":{"vlanId":"4","mode":"Access","vlanServiceAttributes":[{"attributeName":"QnQ","attributeValue":"False","type":"vlanServiceAttribute"},{"attributeName":"CTag","attributeValue":"","type":"vlanServiceAttribute"},{"attributeName":"Allocation Ranges","attributeValue":"2-4094","type":"vlanServiceAttribute"},{"attributeName":"Isolation Level","attributeValue":"Exclusive","type":"vlanServiceAttribute"},{"attributeName":"Access Mode","attributeValue":"Access","type":"vlanServiceAttribute"},{"attributeName":"VLAN ID","attributeValue":"","type":"vlanServiceAttribute"},{"attributeName":"Pool Name","attributeValue":"","type":"vlanServiceAttribute"},{"attributeName":"Virtual Network","attributeValue":"4","type":"vlanServiceAttribute"}],"type":"setVlanParameter"},"connectorAttributes":[],"actionTarget":{"fullName":"super__183bf1","fullAddress":"5.5.5.1","type":"actionTarget"},"customActionAttributes":[{"attributeName":"CreatedBy","attributeValue":"c:usersnoam.wappdatalocaltemptmp_nrzyr.zip_envheavenly_cloud_service_wrapper.py","type":"customAttribute"},{"attributeName":"Reservation Id","attributeValue":"d4e76ed2-e04d-47d5-8cf0-4fe875140c21","type":"customAttribute"},{"attributeName":"VM_UUID","attributeValue":"20f6bf85-c72d-47ad-bfc8-d1f3159e085b","type":"customAttribute"}],"actionId":"3241eb47-3d9a-4dda-becf-b6c010b8622e_76fad88f-f27b-4212-b64f-81ae9a6e6444","type":"setVlan"}]}}'

        parser = DriverRequestParser()

        # act
        actions = parser.convert_driver_request_to_actions(json_req)
        remove_vlan_actions = list(filter(lambda x: isinstance(x, SetVlan), actions))
        # assert
        self.assertIsInstance(remove_vlan_actions[0], SetVlan)

    def test_parse_json_serialized_request(self):
        # prepare
        json_req = '{"driverRequest":{"actions":[{"actionParams":{"appName":"vCenter_CVC_Support","deployment":{"deploymentPath":"VCenter Deploy VM From Linked Clone","attributes":[{"attributeName":"vCenter VM","attributeValue":"Tor/Temps/ImageMonoNew","type":"attribute"},{"attributeName":"vCenter VM Snapshot","attributeValue":"1","type":"attribute"},{"attributeName":"VM Cluster","attributeValue":"","type":"attribute"},{"attributeName":"VM Storage","attributeValue":"","type":"attribute"},{"attributeName":"VM Resource Pool","attributeValue":"","type":"attribute"},{"attributeName":"VM Location","attributeValue":"","type":"attribute"},{"attributeName":"Auto Power On","attributeValue":"True","type":"attribute"},{"attributeName":"Auto Power Off","attributeValue":"True","type":"attribute"},{"attributeName":"Wait for IP","attributeValue":"True","type":"attribute"},{"attributeName":"Auto Delete","attributeValue":"True","type":"attribute"},{"attributeName":"Autoload","attributeValue":"True","type":"attribute"},{"attributeName":"IP Regex","attributeValue":"","type":"attribute"},{"attributeName":"Refresh IP Timeout","attributeValue":"600","type":"attribute"}],"type":"deployAppDeploymentInfo"},"appResource":{"attributes":[{"attributeName":"Password","attributeValue":"3M3u7nkDzxWb0aJ/IZYeWw==","type":"attribute"},{"attributeName":"Public IP","attributeValue":"","type":"attribute"},{"attributeName":"User","attributeValue":"","type":"attribute"}],"type":"appResourceInfo"},"type":"deployAppParams"},"actionId":"ad3561c1-45a5-445a-9b5f-4021879a0b0c","type":"deployApp"}]}}'

        # act
        parser = DriverRequestParser()
        actions = parser.convert_driver_request_to_actions(json_req)

        # assert
        self.assertTrue(len(actions) == 1)
        self.assertEqual(actions[0].actionParams.appName, 'vCenter_CVC_Support')

    def test_try_set_attr(self):
        class CustomModel(object):
            __deploymentModel__ = "VCenter Deploy VM From Linked Clone"

            def __init__(self, attributes):
                self.auto_power_off = attributes['Auto Power Off']
                self.autoload = attributes['Autoload']

        atts_json = '[{"attributeName":"Auto Delete","attributeValue":"True","type":"attributes"},{"attributeName":"Autoload","attributeValue":"True","type":"attributes"},{"attributeName":"IP Regex","attributeValue":"","type":"attributes"},{"attributeName":"Refresh IP Timeout","attributeValue":"600","type":"attributes"},{"attributeName":"vCenter VM","attributeValue":"Tor/Temps/ImageMonoNew","type":"attributes"},{"attributeName":"vCenter VM Snapshot","attributeValue":"1","type":"attributes"},{"attributeName":"VM Cluster","attributeValue":"","type":"attributes"},{"attributeName":"VM Storage","attributeValue":"","type":"attributes"},{"attributeName":"VM Resource Pool","attributeValue":"","type":"attributes"},{"attributeName":"VM Location","attributeValue":"","type":"attributes"},{"attributeName":"Auto Power On","attributeValue":"True","type":"attributes"},{"attributeName":"Auto Power Off","attributeValue":"True","type":"attributes"},{"attributeName":"Wait for IP","attributeValue":"True","type":"attributes"}]'
