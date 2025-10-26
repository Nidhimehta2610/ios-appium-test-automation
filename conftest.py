import pytest
from appium import webdriver
from appium.options.ios import XCUITestOptions

@pytest.fixture(scope="session")
def driver():
    
    options = XCUITestOptions()
    options.platformName = "iOS"
    options.platformVersion = "26.0"        
    options.deviceName = "iPhone 17 Pro"       
    options.app = "/Users/dhruv/Library/Developer/Xcode/DerivedData/Backyard_Birds-ecsykklbqionatgxehvgxzfzacfg/Build/Products/Debug-iphonesimulator/Backyard Birds.app"
    options.automationName = "XCUITest"
    options.noReset = True
    options.w3c = True

    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
    yield driver
    driver.quit()
