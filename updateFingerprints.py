from kubernetes import client, config
import sys
import os

config.load_incluster_config()

with open(sys.argv[1]) as f:
    data = f.read()

config_namespace = os.environ.get("CONFIG_NAMESPACE")
config_name=os.environ.get("CONFIG_MAP")

api_instance = client.CoreV1Api()
cmap = api_instance.read_namespaced_config_map(namespace=config_namespace,name=config_name)
seperator = "# WHITELIST"
newBlock = "\n"+ seperator + data + "\n" + seperator
if "http-snippet" in cmap.data:
    existingconfig = cmap.data["http-snippet"]
    map = existingconfig.split("seperator")
    cmap.data["http-snippet"] = map[0]+ newBlock + map[2]
else:
    cmap.data["http-snippet"] = newBlock

print(cmap)

api_instance.patch_namespaced_config_map(namespace=config_namespace,name=config_name, body=cmap)
