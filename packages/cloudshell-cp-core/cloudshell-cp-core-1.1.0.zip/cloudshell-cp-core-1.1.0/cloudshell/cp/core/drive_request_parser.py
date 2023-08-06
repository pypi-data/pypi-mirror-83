import sys
from cloudshell.cp.core.utils import  *
from cloudshell.cp.core.models import *


class DriverRequestParser:

    def __init__(self):
        self.models_classes = {}
        self.attribute_props = {'attributeName', 'attributeValue'}

    def add_deployment_model(self, deployment_model_cls):
        """
        :param deployment_model_cls: the class you wish to inject to deployment.customModel

        !!! deployment_model_cls must have global str __deploymentModel__
        !!! deployment_model_cls must have attributes in constructor overload

        """

        self.models_classes[deployment_model_cls.__deploymentModel__] = deployment_model_cls

    def convert_driver_request_to_actions(self, driver_request):
        """
        Extracts actions from given driver_request

        :param driver_request:
        :return: [RequestActionBase]
        """

        if isinstance(driver_request, str):
            driver_request = json.loads(driver_request)

        req_actions = driver_request['driverRequest'].get('actions')

        if (req_actions == None):
            return None

        actions_result = []

        for req_action in req_actions:
            class_name = first_letter_to_upper(req_action.get('type'))
            try:
                created_action = getattr(sys.modules[__name__], class_name)()
                self._fill_recursive(req_action, created_action)
                actions_result.append(created_action)

            except Exception as e:
                print (e.message)
                print ('no class named ' + class_name)
                pass

        return  actions_result

    def _create_object_of_type(self, source):
        t = source.get('type')

        if (t == None):
            raise ValueError('source has no "type" property')

        t = first_letter_to_upper(t)
        created = getattr(sys.modules[__name__], t)()

        return created

    def _fill_recursive(self, source, result):
        """
        Fill result from source data ,Recursively!
        :param source: source to read from
        :param result: result to write to

        """
        for key, value in source.items():

            if isinstance(value, dict):
                created = self._create_object_of_type(value)

                # if we are at deployment object, create custom model
                self._handle_deployment_custom_model(created, value)
                set_value(result, key, created)
                self._fill_recursive(value, getattr(result, key))

            elif isinstance(value, (list)):

                if self._try_convert_to_attributes_dict(value, result, key):
                    continue

                created_arr = []
                set_value(result, key, created_arr)

                for item in value:
                    if isinstance(item, (dict)):
                        created_item = self._create_object_of_type(item)
                        created_arr.append(created_item)
                        self._fill_recursive(item, created_item)
                    else:
                        created_arr.append(item)

            else:  # primitive value
                set_value(result, key, value)

    def _handle_deployment_custom_model(self, result, item):

        if item.get('type') != 'deployAppDeploymentInfo':
            return

        atts = item.get('attributes')

        if not atts:
            return

        deployment_model_name = item.get('deploymentPath')

        model_class = self.models_classes.get(deployment_model_name)

        if not model_class:
            return

        result.customModel = model_class(convert_attributes_list_to_dict(atts))

    def _is_attribute(self, item):
        return  self.attribute_props.issubset(item)

    def _try_convert_to_attributes_dict(self, arr, result, key):

        # if not All objects looks like attribute
        if not all(self._is_attribute(item) for item in arr):
            return False

        set_value(result, key, convert_attributes_list_to_dict(arr))

        return True
