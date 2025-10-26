import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#----------------------------------------------------
# S1 — App launch
#----------------------------------------------------
def test_app_launch(driver):
    
    # Wait up to 10 seconds for the home element
    home_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Backyard Birds"))
    )

    # Assert that it is visible
    assert home_element.is_displayed(), "Home screen not displayed"

#----------------------------------------------------
# S2 — List renders
#----------------------------------------------------
def test_list_renders(driver):
    
    # Wait up to 10 seconds for content blocks to load
    blocks = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeStaticText'))
    )

    # Assert that at least one block is present
    assert len(blocks) > 0, "No content blocks found on home page"

#----------------------------------------------------
# S3 — Basic accessibility
#----------------------------------------------------
def test_basic_accessibility(driver):
    
    wait = WebDriverWait(driver, 10)
    home_title = wait.until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Backyard Birds"))
    )
    assert home_title.is_displayed(), "Home title is not accessible"
    print("Home title is locatable and visible")

    # Inspect first cell
    first_cell = wait.until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Bird Springs"))
    )
    assert first_cell.is_displayed(), "First cell 'Bird Springs' is not accessible"
    print("First cell 'Bird Springs' is locatable and visible")
