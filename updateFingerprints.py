from kubernetes import client, config
import sys
import os

config.load_incluster_config()

with open(sys.argv[1]) as f:
    data = f.read()

config_namespace = os.environ.get("CONTROLLER_CONFIG_NAMESPACE")
config_name=os.environ.get("CONTROLLER_CONFIG_MAP")
config_seperator=os.environ.get("CONFIG_SEPERATOR")

if not config_namespace or not config_name:
    print("Config Namespace or Config Map not configured")
else: 
    api_instance = client.CoreV1Api()
    cmap = api_instance.read_namespaced_config_map(name=config_name, namespace=config_namespace)
    seperator = config_seperator
    newBlock = "\n"+ seperator +"\n" + data + seperator+"\n"

    if cmap.data is None:
        cmap.data = {}

    if "http-snippet" in cmap.data:
        existingconfig = cmap.data["http-snippet"]
        map = existingconfig.split(seperator)
        if len(map) == 3:
          cmap.data["http-snippet"] = map[0].strip()+ newBlock + map[2].strip()
        else: 
           cmap.data["http-snippet"] = existingconfig + newBlock
    else:
        cmap.data["http-snippet"] = newBlock
        
    api_instance.patch_namespaced_config_map(namespace=config_namespace,name=config_name, body=cmap)
