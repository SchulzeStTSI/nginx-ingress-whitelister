
import os

class gitRepoEnvMapLoader:
    def load(self) -> dict:
        config={}
        config["X509_CAFILEPATTERN"]=os.environ.get("X509_CAFILEPATTERN")
        config["X509_SOURCEFOLDER"]=os.environ.get("X509_SOURCEFOLDER")
        config["X509_REPO"]=os.environ.get("X509_REPO")
        config["X509_CERTFILEPATTERN"] = os.environ.get("X509_CERTFILEPATTERN")
        return config