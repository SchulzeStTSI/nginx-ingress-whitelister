from kubernetes import client, config
import sys
import os

config.load_incluster_config()

release_name=os.environ.get("RELEASE_NAME")
controller_config_namespace = os.environ.get("CONTROLLER_CONFIG_NAMESPACE")
controller_config_name=os.environ.get("CONTROLLER_CONFIG_MAP")
config_seperator=release_name+"_WHITELIST"

if not controller_config_namespace or not controller_config_name:
    print("Config Namespace or Config Map not configured")
else: 
    api_instance = client.CoreV1Api()
    cmap = api_instance.read_namespaced_config_map(name=controller_config_name, namespace=controller_config_namespace)
    seperator = config_seperator
    if "http-snippet" in cmap.data:
        existingconfig = cmap.data["http-snippet"]
        map = existingconfig.split(seperator)
        if len(map) == 3:
          cmap.data["http-snippet"] = map[0].strip() + map[2].strip()

        httpSnippet = cmap.data["http-snippet"].strip()

        if httpSnippet == "":
            del cmap.data["http-snippet"]
     
    api_instance.replace_namespaced_config_map(namespace=controller_config_namespace,name=controller_config_name, body=cmap)
