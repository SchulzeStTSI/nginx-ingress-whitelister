import os
import glob
import base64
from kubernetes import client, config

config.load_incluster_config()

ingress_namespace = os.environ.get("INGRESS_NAMESPACE")
bundle_secret=os.environ.get("CERTIFICATES_SECRET")

api_instance = client.CoreV1Api()
api_instance.delete_namespaced_secret(namespace=ingress_namespace,name=bundle_secret)
