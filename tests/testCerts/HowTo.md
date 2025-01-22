# Steps

1. generate Key 

```
   openssl ecparam -name prime256v1 -genkey -noout -out ca.key
```

2. Generate CA

```
openssl req -x509 -new -nodes -key ca.key -sha256 -days 1024 -out ca.pem
```

3. Generate Cert Key

```
openssl genrsa -out ClientCert.key 4096
```

4. Create CSR

```
openssl req -new -key ClientCert.key -out ClientCert.csr
```

5. Sign Client Cert

```
openssl x509 -req -in ClientCert.csr -CA ca.pem -CAkey ca.key -CAcreateserial -out ClientCert.pem -days 1024 -sha256
```

6. Optionally pack it as PFX

```
openssl pkcs12 -export -out ClientCert.pfx -inkey ClientCert.key -in ClientCert.pem
```