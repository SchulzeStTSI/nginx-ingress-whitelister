from kubernetes import client, config
import sys
import os

config.load_incluster_config()

namespace = os.environ.get("INGRESS_NAMESPACE")
ingress_name=os.environ.get("INGRESS_NAME")
bundle_secret =  os.environ.get("CERTIFICATES_SECRET")

api_instance = client.NetworkingV1Api()
ingress = api_instance.read_namespaced_ingress(name=ingress_name,namespace=namespace)

if ingress and ingress != None:
   ingress.metadata.annotations["nginx.ingress.kubernetes.io/server-snippet"] = "if ($reject) { return 403; }"
   ingress.metadata.annotations["nginx.ingress.kubernetes.io/auth-tls-secret"] = namespace + "/" + bundle_secret
   ingress.metadata.annotations["nginx.ingress.kubernetes.io/auth-tls-verify-client"] = "on"
   api_instance.patch_namespaced_ingress(name=ingress_name,namespace=namespace, body=ingress)
else: 
   print("Ingress Rule is not existing in the namespace")
