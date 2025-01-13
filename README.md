# Introduction

The usage of client certificates together with nginx ingress controllers is always a long trip to study the documentation and find out what needs to be set. Multiple annotation must be set to enable it, and some more magic must be added to make it secure by certificate pinning. This tool shall do it out of the box:) 

# Features

- [x] Creating a CA Bundle from an predefined Folder
- [x] Creating a Fingerprint List for Certificate Pinning
- [x] Enable automatically Certificate Pinning
- [x] Enable automatically Client Authentication by using Custom CA Bundle
- [x] Update it by sheduled Job

# Usage

Clone the Repository Tag v1 and install the chart by using:

```
helm install  --values val.yaml whitelisting ./k8s
```

The val.yaml is a values file where you can override the default values e.g. : 

```
config:
 tag: v1
certificates:
 repo: https://github.com/{CHANGEME}/{CHANGEME}.git
ingress:
 name: myIngress
job:
 shedule: {yourShedule} # Unix Cron Format
```
More about the Cron Format can you find [here](https://en.wikipedia.org/wiki/Cron) 

# Scripts

## General Parameters

|Parameter|Description|
|---------|--------------|
|NAMESPACE|Name of the namespace where the ingress rule and the bundle is located (secrets can be shared between namespaces)|
|CERTIFICATES_SECRET | A bundle of tls pem strings which is configured in a kubernetes secret. |
|CERTIFICATES_REPO| Repo where the certificates are located|
|INGRESS_NAME| The name of the ingress rule which is applied.|
|CONTROLLER_CONFIG_MAP| This variable defines the config map of the ingress controller to set controller specific settings within nginx. |
|CONTROLLER_CONFIG_NAMESPACE| Namespace where the nginx controller is located. |
|TAG| Tag of the ngnix whitlister version which the bot is using.|
|REPO| Repo of the whitelister branches|
|RELEASE_NAME| Release name of the helm deployment |

## Description

|Script|Description|
|----------|----------|
|[Annotate ingress](./annotateIngress.py) | Searches for an ingress rule in a namespace and annotates the nginx ingress rule with the certificate bundle which was uploaded/defined in a secret. This secret is configured in the [auth-tls](https://github.com/kubernetes/ingress-nginx/blob/main/docs/user-guide/nginx-configuration/annotations.md#client-certificate-authentication) annotation of the rule to unlock traffic protected by the configured certificate.|
|[Fingerprint](fingerprints.sh)| generates for nginx an fingerprint mapping across all certificates in the folder, which is later on configured in the configuration snippets of the ingress configuration map [http-snippet](https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/configmap/#http-snippet) (default located unter: nginx-ingress/addon-http-application-routing-nginx-configuration or similar)|
|[Remove CA Bundle](removeCaBundle.py)| removes the Bundle Secret from the namespace during uninstall of the helm package.|
|[Remove Fingerprints](removeFingerprints.py)| removes the fingerprints von the nginx config during the uninstall of the helm package.|
|[Remove Ingress Annotation](removeIngressAnnotation.py)| removes the annotations from the rule which is observed.|
|[Update CA Bundle](updateCaBundle.py)| updates the bundle secret with the latest packages found in certificate folder|
|[Update Fingerprints](updateFingerprints.py)| updates the fingerprints in the controller config seperated by the config_seperator|


# Test Setup 

## Helm

Install on your device the helm software for installing helm charts.

## Kubernetes 

Install for testing the latest ranger desktop and follow the [nginx install instructions](https://docs.rancherdesktop.io/how-to-guides/setup-NGINX-Ingress-Controller/). Alternativly k3s or minikube works as well.

## Pytest

Install pytest and navigate to the tests folder. Execute it by pytest or by using python -m pytest.

