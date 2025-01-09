import os
import glob
import base64
from kubernetes import client, config

config.load_incluster_config()

ingress_namespace = os.environ.get("INGRESS_NAMESPACE")
bundle_secret=os.environ.get("CERTIFICATES_SECRET")
files = glob.glob("./certificateFolder/**/TLS/CA*.pem", recursive=True)
ca_bundle = ""
for file in files:
  with open(file) as f:
    data = f.read()
  ca_bundle = ca_bundle+"\n"+data
  
if len(files) and ca_bundle:
  api_instance = client.CoreV1Api()
  body = client.V1Secret()
  body.api_version = 'v1'
  body.data = {'ca.crt': str(base64.b64encode(bytes(ca_bundle,"utf-8")),"utf-8")}
  body.kind = 'Secret'
  body.type = 'Opaque'
  api_instance.patch_namespaced_secret(namespace=ingress_namespace,name=bundle_secret, body=body)
else: 
  print("No files found or empty CA bundle")
    
