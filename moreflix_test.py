import subprocess
import time
import pytest
import requests
import json

@pytest.fixture(scope="session", autouse=True)
def docker_compose():
    subprocess.check_call(["docker", "volume", "rm", "-f", "moreflix_moreflix"])

    """
    This fixture starts Docker Compose before any tests run
    and tears it down after the tests complete.
    """
    subprocess.check_call(["docker", "build", "-t", "moreflix:test-1.0", "."])

    # Bring up the services in detached mode
    subprocess.check_call(["docker", "compose", "-f", "docker-compose-test.yml", "up", "-d"])
    
    # Optionally, wait until services are ready (adjust the sleep duration or use a smarter health check)
    time.sleep(10)
    
    yield  # Run the tests
    
    # Tear down the Docker Compose environment
    subprocess.check_call(["docker-compose", "-f", "docker-compose-test.yml", "down"])

def test_service_health():
    """
    Example test that checks if a service is responding.
    Replace 'http://localhost:5000/test' with the actual URL of your service.
    """
    response = requests.get("http://localhost:5000/")
    assert response.status_code == 200

    response = requests.get("http://localhost:5000/api/v1/findall")
    assert response.status_code == 200

    json_data = response.json()

    assert len(json_data) == 10, "Expected 10 records but got {0}".format(len(json_data))


    
