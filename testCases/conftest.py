import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from TestData.Secrets import Secrets

driver = None


def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", action="store", default="chrome"
    )
    parser.addoption(
        "--environment", action="store", default="beta"
    )
    parser.addoption(
        "--wait_time", action="store", default=10
    )


@pytest.fixture(scope="class")
def setup(request):
    global driver
    browser_name = request.config.getoption("browser_name")
    wait_time = request.config.getoption("wait_time")
    if browser_name == "chrome":
        driver_service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=driver_service)
        driver.implicitly_wait(wait_time)
    elif browser_name == "firefox":
        service = Service(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service)
        driver.implicitly_wait(wait_time)
    elif browser_name == "edge":
        service = Service(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service)
        driver.implicitly_wait(wait_time)
    if request.config.getoption("environment") == "test":
        link = f"https://{Secrets.webauth}@testcn-new.tme.hk"
    elif request.config.getoption("environment") == "prod":
        link = "https://tme.cn"
    else:
        link = f"https://{Secrets.webauth}@betacn-new.tme.hk/"
    driver.get(link)
    request.cls.driver = driver
    yield
    driver.close()
