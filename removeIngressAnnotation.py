from kubernetes import client, config
from kubernetes.client.exceptions import ApiException
import sys
import os

config.load_incluster_config()

ingress_namespace = os.environ.get("INGRESS_NAMESPACE")
ingress_name=os.environ.get("INGRESS_NAME")

api_instance = client.NetworkingV1Api()
try: 
   ingress = api_instance.read_namespaced_ingress(name=ingress_name,namespace=ingress_namespace)

   if ingress:
      if ingress.metadata.annotations["nginx.ingress.kubernetes.io/server-snippet"]:
         del ingress.metadata.annotations["nginx.ingress.kubernetes.io/server-snippet"]
      if ingress.metadata.annotations["nginx.ingress.kubernetes.io/auth-tls-secret"]:
         del ingress.metadata.annotations["nginx.ingress.kubernetes.io/auth-tls-secret"]
      if ingress.metadata.annotations["nginx.ingress.kubernetes.io/auth-tls-verify-client"]:
         del ingress.metadata.annotations["nginx.ingress.kubernetes.io/auth-tls-verify-client"]
      api_instance.replace_namespaced_ingress(name=ingress_name,namespace=ingress_namespace, body=ingress)
   else: 
      print("Ingress Rule is not existing in the namespace")

except ApiException as e:
    if e.status == 404:
        print(f"Ingress '{ingress_name}' im Namespace '{ingress_namespace}' not existing.")
        ingress = None
    else:
        print(f"An error was raised: {e}")
        raise