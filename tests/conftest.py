
import pytest
import time
from base.webdriverfactory import WebDriverFactory
from pages.home.login_page import LoginPage

@pytest.yield_fixture()
def setUp():
    print("\nRunning method level setUp")
    yield
    print("\nRunning method level tearDown")


@pytest.yield_fixture(scope="class")
def oneTimeSetUp(request, browser):
    print("\nRunning one time setUp")
    wdf = WebDriverFactory(browser)
    driver = wdf.getWebDriverInstance()
    # get variables from data.json
    lp = LoginPage(driver)

    lp.newLogPage()  # print header for new line for new log of new test.


    lp.clickUpLoginButton() # UP RIGHT button on Home page;


    creden = lp.get_data()["right_cr"]
    lp.login(creden["user"], creden["pass"])

    # Pop up after first log in
    # Find element 'close' and click
    try:
        lp.waitForClickElement("//button[@title='Close']", True)
    except:
        print("Element close not found.")


    if request.cls is not None:
        request.cls.driver = driver
    yield driver
    driver.quit()
    print("\nRunning one time tearDown")

def pytest_addoption(parser):
    parser.addoption("--browser")
    parser.addoption("--osType", help="Type of operating system")

@pytest.fixture(scope="session")
def browser(request):
    return request.config.getoption("--browser")

@pytest.fixture(scope="session")
def osType(request):
    return request.config.getoption("--osType")