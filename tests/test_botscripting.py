import pytest
from testUtils import helm_chart, wait_for_job_log

# Pytest test
@pytest.mark.parametrize("release_name,deployment_name,helm_chart_values,values_file", [
    ("my-release", "test-deployment", {"replicaCount": 2}, "./values.yaml")
])
def test_helm_chart(helm_chart, release_name, deployment_name, helm_chart_values, values_file):
    namespace = "test-namespace"
    chart_path = "../helm"  # Path to your testDeployment chart

    # Install Helm chart
    helm_chart(release_name, chart_path, namespace, helm_chart_values, values_file=values_file)

    # Wait for log message
    found = wait_for_job_log(deployment_name, namespace, "Source Folder and/or certFilePattern empty. Skip the fingerprint pinning")

    # Assert the result
    assert found, f"Expected log message not found after {20} attempts."

if __name__ == "__main__":
    pytest.main(["-v", __file__])