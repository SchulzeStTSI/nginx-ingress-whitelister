# IOC

Inversion of control container which can be enabled over an json: 

```
{
  "service_interface": {
    "do_work": {
      "parameters": ["str", "int"]
    },
    "send_email": {
      "parameters": ["str", "str"]
    }
  }
}
```

After that the containers accept various implementations. Which can be registered via filename or classname: 

```
ioc = IoCContainer(json_file='interface.json')

# Register services dynamically by module path
ioc.register("database_service", "./database.py")  # Path to the Python file
ioc.register("email_service", "./email.py")  # Path to the Python file

# Register services by class name within the code base
ioc.register("database_service", "database.DatabaseService")  # Class name as a string
ioc.register("email_service", "email.EmailService")  # Class name as a string

# List the services to verify registration
print(ioc.list_services())
```

Json: 

```
{
  "database_service": {
    "functions": {
      "do_work": {
        "parameters": [
          {"name": "message", "type": "str"},
          {"name": "count", "type": "int"}
        ]
      }
    }
  },
  "email_service": {
    "functions": {
      "send_email": {
        "parameters": [
          {"name": "recipient", "type": "str"},
          {"name": "subject", "type": "str"}
        ]
      }
    }
  }
}

```
