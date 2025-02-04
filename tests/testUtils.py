### File: helm_utils.py
import subprocess
import time
from kubernetes import client, config
### Fixtures for Helm management
import pytest
import os

# Function to install a Helm chart with optional values and a values file
def install_helm_chart(release_name, chart_path, namespace, values=None, values_file=None):
    cwd = os.getcwd()
    chart_path  = os.path.join(cwd,chart_path)

    command = [
        "helm", "dependency", "build", chart_path
    ]

    try:
        subprocess.run(command, check=True, stderr=subprocess.PIPE, text=True)
    except subprocess.CalledProcessError as e:
     print(f"Fehler: {e}")  # Gibt die Exception aus
     return

    command = [
        "helm", "install", release_name, chart_path, "-n", namespace, "--create-namespace"
    ]
    if values:
        for key, value in values.items():
            command.extend(["--set", f"{key}={value}"])
    if values_file:
        vF = os.path.join(cwd,values_file)
        command.extend(["-f", vF])
    try:
        subprocess.run(command, check=True, stderr=subprocess.PIPE, text=True)
    except subprocess.CalledProcessError as e:
     print(f"Fehler: {e}")  # Gibt die Exception aus

# Function to uninstall a Helm chart
def uninstall_helm_chart(release_name, namespace):
    subprocess.run([
        "helm", "uninstall", release_name, "-n", namespace
    ], check=True)

# Function to wait for a specific log message in a Kubernetes job
def wait_for_job_log(job_name, namespace, search_text, timeout=60, interval=10):
    config.load_kube_config()
    v1 = client.CoreV1Api()

    attempts = 0
    while attempts < (timeout // interval):
        try:
            pod_list = v1.list_namespaced_pod(namespace, label_selector=f"job-name={job_name}")
            for pod in pod_list.items:
                pod_name = pod.metadata.name
                log = v1.read_namespaced_pod_log(pod_name, namespace)

                if search_text in log:
                    return True
        except client.exceptions.ApiException as e:
            print(f"Error fetching logs: {e}")

        attempts += 1
        time.sleep(interval)

    return False

# Generic reusable fixture for installing Helm charts
@pytest.fixture(scope="function")
def setup_helm_chart():
    def _setup(release_name, chart_path, namespace, values=None, values_file=None):
        install_helm_chart(release_name, chart_path, namespace, values, values_file)
        return namespace

    yield _setup

# Generic reusable fixture for cleaning up Helm charts
@pytest.fixture(scope="function")
def teardown_helm_chart():
    def _teardown(release_name, namespace):
        uninstall_helm_chart(release_name, namespace)

    yield _teardown

# Combined setup and teardown fixture for tests
@pytest.fixture(scope="function")
def helm_chart(setup_helm_chart, teardown_helm_chart):
    created_releases = []

    def _manage(release_name, chart_path, namespace, values=None, values_file=None):
        namespace = setup_helm_chart(release_name, chart_path, namespace, values, values_file)
        created_releases.append((release_name, namespace))
        return namespace

    yield _manage

    for release_name, namespace in created_releases:
        teardown_helm_chart(release_name, namespace)