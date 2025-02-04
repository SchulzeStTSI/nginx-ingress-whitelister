# Load configured dids from the pre mounted config map

import os 
from kubernetes import client, config

class ConfigMapLoader:
    def load(self) -> dict:
        namespace = os.environ.get("INGRESS_NAMESPACE")
        config_map_name= os.environ.get("CONFIG_MAP")

        config.incluster_config.load_incluster_config()

        # Get the CoreV1Api client
        v1 = client.CoreV1Api()

        try:
            # Fetch the ConfigMap
            config_map = v1.read_namespaced_config_map(config_map_name, namespace)

            # Convert the ConfigMap's data field into a Python dictionary
            config_map_dict = config_map.data

            # Return the dictionary containing the key-value pairs of the ConfigMap
            return config_map_dict

        except client.exceptions.ApiException as e:
            print(f"An error occurred while reading the ConfigMap: {e}")
            return {}