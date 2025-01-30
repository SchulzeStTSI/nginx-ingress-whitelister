# Clones Key Repo and provides it to certificate Folder
import os 
import glob

import uuid 

class x509Loader:
    def loadKeys(self,config:dict):
        try: 
            
            temp_dir = config["TMPDIR"]
            caPath = config["CADIR"]
            tlsPath = config["TLSDIR"]
            caPattern=config["X509_CAFILEPATTERN"]
            sourceFolder=config["X509_SOURCEFOLDER"]
            certRepo=config["X509_REPO"]
            certFilePattern=config["X509_CERTFILEPATTERN"]
            certRepoFolder= os.path.join(temp_dir,"certrepo")

            os.system("git clone "+certRepo +" "+certRepoFolder)

            files = glob.glob(certRepoFolder+"/**/"+sourceFolder+"/"+caPattern, recursive=True)
        
            for file in files:
                random_filename = f"{uuid.uuid4().hex}.pem"
                with open(file) as f:
                    data = f.read()
                    with open(os.path.join(caPath,random_filename),"w") as file:
                      file.write(data)


            files = glob.glob(certRepoFolder+"/**/"+sourceFolder+"/"+certFilePattern, recursive=True)

            for file in files:
                random_filename = f"{uuid.uuid4().hex}.pem"
                with open(file) as f:
                    data = f.read()
                    with open(os.path.join(tlsPath,random_filename),"w") as file:
                     file.write(data)
        except:
            raise