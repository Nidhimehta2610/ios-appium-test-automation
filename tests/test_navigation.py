from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#-----------------------------------------------------------
    # N1 — Open first detail & go back
#-----------------------------------------------------------
def test_open_first_detail_and_go_back(driver):
    wait = WebDriverWait(driver, 10)

    # Tap first cell
    first_cell = wait.until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Bird Springs")))
    first_cell.click()
    print("Tapped first cell.")

    # Verify detail header
    detail_header = wait.until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Bird Springs")))
    assert detail_header.is_displayed(), "Detail header is not visible"

    # Go back
    backbutton = wait.until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "BackButton")))
    backbutton.click()

    # Verify home screen element
    home_label = wait.until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Backyard Birds")))
    assert home_label.is_displayed(), "Home screen not visible"
    
#-----------------------------------------------------------
    # N2 — Scroll list (down/up)
#-----------------------------------------------------------
def test_scroll_list(driver):
    wait = WebDriverWait(driver, 10)

    # Locate the scrollable list
    scroll_view = wait.until(
        EC.presence_of_element_located((AppiumBy.CLASS_NAME, "XCUIElementTypeScrollView")))
    assert scroll_view.is_displayed(), "Scroll view is not visible initially"

    # Scroll down
    driver.execute_script("mobile: scroll", {"direction": "down"})
    print("Scrolled down successfully")

    # Scroll up
    driver.execute_script("mobile: scroll", {"direction": "up"})
    print("Scrolled up successfully")

    # Simple assertion: verify the scroll view is still visible
    assert scroll_view.is_displayed(), "Scroll view disappeared after scrolling!"
    print("Scroll view is still visible after scrolling")

#-----------------------------------------------------------
    # N3 — Deep navigation path
#-----------------------------------------------------------
def test_deep_navigation(driver):    
    wait = WebDriverWait(driver, 10)

    # Open item A
    item_a = wait.until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Bird Springs"))
    )
    item_a.click()

    # Verify title for item A
    title_a = wait.until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Bird Springs")))
    assert title_a.is_displayed(), "Item A is not visible"

    # Go back
    back_button = wait.until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "BackButton")))
    assert back_button.is_displayed(), "Back button is not visible"
    back_button.click()

    # Open item B
    item_b = wait.until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Feathered Friends")))
    item_b.click()

    # Verify title for item B
    title_b = wait.until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Feathered Friends")))
    assert title_b.is_displayed(), "Item B is not visible"

    # Verify back button still works and is visible
    back_button_b = wait.until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "BackButton")))
    assert back_button_b.is_displayed(), "Back button is not visible"
    back_button_b.click()

#-----------------------------------------------------------
    # N5 — External entry
#-----------------------------------------------------------
def test_simple_external_entry(driver):
    wait = WebDriverWait(driver, 10)

    # Open detail page (Bird Springs)
    bird_springs = wait.until(
        EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Bird Springs"))).click()
    print("Opened detail page for Bird Springs.")

    # Tap in-app button (Sunflower Seeds)
    sunflower_seeds = wait.until(
        EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Sunflower Seeds"))).click()
    print("Tapped on Sunflower Seeds.")

    # Verify Bird Food screen appears
    bird_food_header = wait.until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Bird Food")))
    assert bird_food_header.is_displayed(), "Bird Food screen did not appear"
    print("Bird Food screen is visible.")

    # Navigate back to Bird Springs detail
    driver.back() 
    detail_header = wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Bird Springs")))
    assert detail_header.is_displayed(), "Did not return to Bird Springs detail" 

    # Navigate back to home
    driver.back()
    home_screen = wait.until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Backyard Birds")))
    assert home_screen.is_displayed(), "Home screen not visible"
   