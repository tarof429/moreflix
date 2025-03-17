import pytest
import pycurl
import os
from io import BytesIO

@pytest.fixture(scope="session")
def before():

    curl = pycurl.Curl()
    curl.setopt(pycurl.URL, 'http://moreflix:5000/api/dropdb')

    curl.perform()
    curl.close()

def test_get_all_movies():
    buffer = BytesIO()

    curl = pycurl.Curl()

    curl.setopt(pycurl.URL, 'http://moreflix:5000/api/createdb')
    curl.perform()
    
    curl.setopt(pycurl.URL, 'http://moreflix:5000/api/findall')
    curl.setopt(pycurl.WRITEDATA, buffer)
    curl.perform()

    assert curl.getinfo(curl.RESPONSE_CODE) == 200

    curl.close()