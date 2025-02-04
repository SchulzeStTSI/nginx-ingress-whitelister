# Loads DIDs from Config List
import requests
import urllib.parse
import re
import os 
import uuid 

class didLoader:

    def fetch_json(self,base_url, path_param):
        try:
            url = f"{base_url}/{path_param}"  # Path-Parameter in die URL einfügen
            response = requests.get(url)
            response.raise_for_status()  # Löst eine Ausnahme aus, wenn der HTTP-Statuscode nicht 200 ist
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

    def filter_verification_methods(did_document, key_pattern):
        pattern = re.compile(key_pattern)
        return [
            method for method in did_document.get("verificationMethod", [])
            if method.get("id") and pattern.search(method.get("id").split("#")[-1])
        ]
    
    def extract_x5c_and_write_pem(self,verification_methods, output_file):
        with open(output_file, "w") as pem_file:
            for method in verification_methods:
                x5c_certs = method.get("x5c", [])
                for cert in x5c_certs:
                    pem_file.write("-----BEGIN CERTIFICATE-----\n")
                    pem_file.write("\n".join([cert[i:i+64] for i in range(0, len(cert), 64)]))
                    pem_file.write("\n-----END CERTIFICATE-----\n\n")

    def loadKeys(self,config:dict):
       
        keys_to_check = ["TMPDIR", 
                         "CADIR", 
                         "TLSDIR",
                         "DID_DOC_DIDS","DID_DOC_VER_TLS_FILTER","DID_DOC_VER_CA_FILTER","DID_DOC_RESOLVER_URL"]
        
        if all(key in config for key in keys_to_check):
             print("All keys are present.")
        else:
            print("Some keys are missing.")
            return

        temp_dir = config["TMPDIR"]
        caPath = config["CADIR"]
        tlsPath = config["TLSDIR"]
        verifcationMethods = config["DID_DOC_DIDS"]
        caFilter = config["DID_DOC_VER_CA_FILTER"]
        tlsFilter = config["DID_DOC_VER_TLS_FILTER"]
        resolverUrl = config["DID_DOC_RESOLVER_URL"]

        dids = [service.strip() for service in verifcationMethods.split(",")]
        tlsPattern = [service.strip() for service in tlsFilter.split(",")]
        caPattern = [service.strip() for service in caFilter.split(",")]

        for did in dids: 
            random_filename = f"{uuid.uuid4().hex}.pem"
            try: 
               doc = self.fetch_json(resolverUrl,did)
               for ca in caPattern:
                methods = self.filter_verification_methods(doc,ca)
                if len(methods) == 0: 
                     print(f"No ca keys found for "+did)
                self.extract_x5c_and_write_pem(methods,os.path.join(caPath,random_filename))
                
               for tls in tlsPattern:
                methods = self.filter_verification_methods(doc,tls)
                if len(methods) == 0: 
                     print(f"No tls keys found for "+did)
                if len(methods)==1:
                    self.extract_x5c_and_write_pem(methods,os.path.join(tlsPath,random_filename))
                if len(methods)>1: 
                    self.extract_x5c_and_write_pem(methods[:1],os.path.join(tlsPath,random_filename))
                    self.extract_x5c_and_write_pem(methods[1:],os.path.join(caPath,random_filename))
            except Exception as e:
                print(f"Error fetching data: {e}")