from kubernetes import client, config
from kubernetes.client.exceptions import ApiException
import sys
import os

config.load_incluster_config()

namespace = os.environ.get("INGRESS_NAMESPACE")
ingress_name=os.environ.get("INGRESS_NAME")
certificates_secret =  os.environ.get("CERTIFICATES_SECRET")

api_instance = client.NetworkingV1Api()
try: 
   ingress = api_instance.read_namespaced_ingress(name=ingress_name,namespace=namespace)

   if ingress and ingress != None:
      ingress.metadata.annotations["nginx.ingress.kubernetes.io/server-snippet"] = "if ($reject) { return 403; }"
      ingress.metadata.annotations["nginx.ingress.kubernetes.io/auth-tls-secret"] = namespace + "/" + certificates_secret
      ingress.metadata.annotations["nginx.ingress.kubernetes.io/auth-tls-verify-client"] = "on"
      api_instance.patch_namespaced_ingress(name=ingress_name,namespace=namespace, body=ingress)
   else: 
      print("Ingress Rule is not existing in the namespace")

except ApiException as e:
    if e.status == 404:
        print(f"Ingress '{ingress_name}' im Namespace '{namespace}' not existing.")
        ingress = None
    else:
        print(f"Ein Fehler ist aufgetreten: {e}")
        raise