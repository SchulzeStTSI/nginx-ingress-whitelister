# Loads DIDs from Config List

class didLoader:
    def loadKeys(self,config:dict):
         temp_dir = config["TMPDIR"]
         caPath = config["CADIR"]
         tlsPath = config["TLSDIR"]