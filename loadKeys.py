import os
from internal.ioc import IoCContainer
from collections import ChainMap
import tempfile
import sys

if len(sys.argv) > 1:
       jsonF = sys.argv[1]
else: 
      jsonF = "./internal/interface.json"



# Initialize the IoC container with the interface file
ioc = IoCContainer(services_json_file=jsonF)

# Get the environment variable for services to load
configLoader = os.getenv("CONFIG_CONFIGLOADER", "")

# Check if the environment variable is not empty
if not configLoader:
    print("No services to load. Please set the SERVICES_TO_LOAD environment variable.")
    raise

# Split the comma-separated list of services
configLoaderServices = [service.strip() for service in configLoader.split(",")]

# Register the services dynamically based on the environment variable
for service_name in configLoaderServices:
        ioc.register("configLoader", service_name)
    

# Get the environment variable for services to load
pubKeyLoader = os.getenv("CONFIG_PUBKEYLOADER", "")

# Check if the environment variable is not empty
if not pubKeyLoader:
    print("No services to load. Please set the SERVICES_TO_LOAD environment variable.")
    raise

# Split the comma-separated list of services
pubKeyLoaderServices = [service.strip() for service in pubKeyLoader.split(",")]

# Register the services dynamically based on the environment variable
for service_name in pubKeyLoaderServices:
        ioc.register("pubKeyLoader", service_name)

# List all services registered in the container
print(f"Services registered: {ioc.list_services()}")

if len(sys.argv) > 2:
       tmpPath = sys.argv[2]
else: 
      tmpPath = tempfile.mktemp()
      os.mkdir(tmpPath)

configLoaderServices = ioc.get_all("configLoader")

caPath = os.path.join(tmpPath,"CA")
tlsPath= os.path.join(tmpPath,"TLS")
config={}
config["TMPDIR"] =  tmpPath
config["CADIR"] =  caPath
config["TLSDIR"] = tlsPath
os.mkdir(caPath)
os.mkdir(tlsPath)
for service in configLoaderServices:
     tC= service.load()
     config = ChainMap(config, tC)


pubKeyLoaderServices = ioc.get_all("pubKeyLoader")

for service in pubKeyLoaderServices:
   dir= service.loadKeys(config)