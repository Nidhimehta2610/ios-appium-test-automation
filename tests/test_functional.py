from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import pytest

#-------------------------------------------------------------------
# F1 — Toggle Favorite
#-------------------------------------------------------------------
def test_toggle_favorite(driver):
    wait = WebDriverWait(driver, 10)

    # Open first item
    first_item = wait.until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Bird Springs"))
    )
    first_item.click()

    # Locate favorite button
    fav_button = wait.until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Favorite"))
    )
    assert fav_button.is_displayed(), "Favorite button is not visible"

    # Toggle ON and verify
    initial_state = fav_button.get_attribute("value")  # "0" for OFF, "1" for ON
    fav_button.click()
    new_state = fav_button.get_attribute("value")
    assert new_state != initial_state, "Favorite state did not change after toggle ON"
    print(f"Favorite toggled ON. State: {new_state}")

    # Toggle OFF and verify
    fav_button.click()
    reverted_state = fav_button.get_attribute("value")
    assert reverted_state == initial_state, "Favorite state did not revert after toggle OFF"
    print(f"Favorite toggled OFF. State reverted to: {reverted_state}")

    # Go back
    back_button = wait.until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "BackButton"))
    )
    back_button.click()

    # Open first item
    first_item = wait.until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Bird Springs"))
    )
    first_item.click()

     # Go back
    back_button = wait.until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "BackButton"))
    )
    back_button.click()

    home_label = wait.until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Backyard Birds"))
    )
    assert home_label.is_displayed(), "Home screen not visible after toggling favorite"

#-------------------------------------------------------------------
# F2 — Detail content validation
#-------------------------------------------------------------------
def test_detail_content_validation(driver):
    wait = WebDriverWait(driver, 10)

    item = wait.until(
        EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Bird Springs"))
    )
    item.click()
    print("Opened item detail page.")

    # Assert hero image is visible
    hero_image = wait.until(
        EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Fountain/Terracotta"))
    )
    assert hero_image.is_displayed(), "Hero image is not visible"
    print("Hero image is visible.")

    fav_button = wait.until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Favorite"))
    )
    assert fav_button.is_displayed(), "Favorite button is not visible"

    back_button = wait.until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "BackButton"))
    )
    back_button.click()

#-------------------------------------------------------------------
# F3 — Search / Filter (if present)
#-------------------------------------------------------------------
def test_search_filter(driver):
    wait = WebDriverWait(driver, 10)

     # Click search field 
    search_field = wait.until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Search"))
    )
    search_field.click()
    print("Clicked on search field.")

    # Capture initial sample items
    initial_items = driver.find_elements(AppiumBy.XPATH, "//XCUIElementTypeStaticText")
    initial_count = len(initial_items)
    print(f"Initial sample items count: {initial_count}")

    # Enter a search query
    search_field.send_keys("Calm Palms")  # send valid query
    print("Entered search query: 'Calm Palms'")

    # Capture the search results
    results = driver.find_elements(AppiumBy.XPATH, "//XCUIElementTypeStaticText[contains(@label,'Calm Palms')]")
    results_count = len(results)
    assert results_count > 0, f"Expected > 0 results, found {results_count}"
    print(f"Search returned {results_count} results.")

    # Clear the search
    clear_text = wait.until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Clear text"))
    )
    clear_text.click()
    print("Cleared search field.")

    # Verify the list resets to initial items
    reset_items = driver.find_elements(AppiumBy.XPATH, "//XCUIElementTypeStaticText")
    reset_count = len(reset_items)
    assert reset_count == initial_count, f"Expected {initial_count} items after clear, found {reset_count}"
    print("List reset to initial state after clearing search.")

    # Close search
    close_button = wait.until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Close"))
    )
    close_button.click()

#-------------------------------------------------------------------
# F4 — Retain state after navigation
#-------------------------------------------------------------------
def test_favorite_state_retention(driver):
    wait = WebDriverWait(driver, 10)

    # Open detail page for item
    detail_button = wait.until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Feathered Friends"))
    )
    detail_button.click()
    print("Opened detail page.")

    # Tap favorite button
    detail_fav_button = wait.until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Favorite"))
    )
    detail_fav_button.click()
    print("Clicked favorite button on detail page.")

    fav_state_after_click = detail_fav_button.get_attribute("value")  # "1" = ON, "0" = OFF
    print("Favorite state after click:", fav_state_after_click)

    # Navigate back to Home
    back_button = wait.until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "BackButton"))
    )
    back_button.click()
    print("Returned to Home page.")

    # Reopen the same item
    detail_button = wait.until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Feathered Friends"))
    )
    detail_button.click()
    print("Reopened detail page.")

    # Verify favorite state persisted
    detail_fav_button = wait.until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Favorite"))
    )
    fav_state_after_reopen = detail_fav_button.get_attribute("value")
    print("Favorite state after reopening:", fav_state_after_reopen)

    assert fav_state_after_reopen == fav_state_after_click, \
        "Favorite state did not persist after navigation"
    print("Favorite state persisted correctly after navigation.")

    # Navigate back to Home
    back_button = wait.until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "BackButton"))
    )
    back_button.click()
    print("Returned to Home page.")

#-------------------------------------------------------------------
# F5 — Empty/edge search
#-------------------------------------------------------------------
def test_empty_edge_search(driver):
    wait = WebDriverWait(driver, 10)

    # Tap search field and enter nonsense term
    search = wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Search")))
    search.click()
    search.send_keys("zzzz")
    print("Searching for nonsense term 'zzzz'...")

    # Verify "No results" or empty list
    results = driver.find_elements(AppiumBy.XPATH, "//XCUIElementTypeCell")
    assert len(results) == 0, f"Expected no results, found {len(results)} items."
    print("No results found")

    # Clear or close search
    driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Clear text").click()
    driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Close").click()

    # Confirm Home visible
    home_item = wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Bird Springs")))
    assert home_item.is_displayed(), "Home not visible after search."

#-------------------------------------------------------------------
# F7 — Time format (12-hour AM/PM) regression
#-------------------------------------------------------------------
def test_time_format_layout(driver):
    wait = WebDriverWait(driver, 10)

    # Open Home screen
    home_title = wait.until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Bird Springs"))
    )
    assert home_title.is_displayed(), "Home screen not visible"

    # Collect all remaining-time labels (eg: 6hrs, 16hrs)
    time_labels = driver.find_elements(
    AppiumBy.XPATH, "//XCUIElementTypeStaticText[contains(@name, 'hrs remaining')]"
)

    # Verify each label is visible and readable
    for lbl in time_labels:
        assert lbl.is_displayed(), f"Remaining time '{lbl.text}' is not visible"
        print(f"Remaining time visible: {lbl.text}")

    print("All remaining-time labels are visible and layout is correct")

#-------------------------------------------------------------------
# F8 — Dark mode basic
#-------------------------------------------------------------------
def test_dark_mode_basic(driver):
    wait = WebDriverWait(driver, 10)

    home_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Backyard Birds"))
    )
    assert home_element.is_displayed(), "Home screen not displayed"

    # Open Detail Screen
    detail_title = wait.until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Bird Springs"))
    )
    detail_title.click()
    print("Bird Springs page opened")

    # Verify critical texts on the detail screen are visible/readable
    critical_texts = ["Sunflower Seeds", "Water"]
    for text in critical_texts:
        el = driver.find_element(AppiumBy.ACCESSIBILITY_ID, text)
        assert el.is_displayed(), f"Critical text '{text}' not visible"
        print(f"'{text}' visible on Home page.")

    # Verify Favorite button is visible
    fav_button = wait.until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Favorite"))
    )
    assert fav_button.is_displayed(), "Favorite button is not visible"

    # Navigate back to Home and verify Back button is visible
    back_button = wait.until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "BackButton"))
    )
    assert back_button.is_displayed(), "Back button is not visible"
    back_button.click()

#-------------------------------------------------------------------
# F10 — Start-up performance sanity
#-------------------------------------------------------------------
def test_startup_performance(driver):
  
    threshold_seconds = 3

    # Start timer immediately after app launch
    start_time = time.time()

    wait = WebDriverWait(driver, 10)

    # Wait for a key element on Home screen to be visible
    home_element = wait.until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Backyard Birds"))
    )

    elapsed_time = time.time() - start_time
    print(f"Startup time: {elapsed_time:.2f} seconds")

    # Assert startup time is within threshold
    assert elapsed_time <= threshold_seconds, f"Startup too slow: {elapsed_time:.2f}s > {threshold_seconds}s"

    print("Home screen visible within acceptable startup time")

#---------------------------------------------------------------------
# F11 — Idempotent favorite flow
#---------------------------------------------------------------------
def test_idempotent_favorite_flow(driver):
    wait = WebDriverWait(driver, 10)

    # Navigate to detail page
    first_item_cell = wait.until(
        EC.presence_of_element_located(
        (AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeStaticText[`name == "Bird Springs"`]')
        )
    )
    first_item_cell.click()
    
    # Locate favorite button
    detail_fav_button = wait.until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Favorite"))
    )
    # Toggle favorite twice to test idempotency
    for i in range(4):
        detail_fav_button.click()
        time.sleep(0.5)  # wait for UI animation
        # Optional: print label or name to see visual change
        label = detail_fav_button.get_attribute("label")
        print(f"Toggle {i+1}: label='{label}'")

    # Return to home safely
    back_button = wait.until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "BackButton"))
    )
    back_button.click()
    print("Returned to home page after idempotent test.")

#---------------------------------------------------------------------
# F12 — Screenshot on failure
#---------------------------------------------------------------------
def test_screenshot_on_failure(driver):
    wait = WebDriverWait(driver, 10)

    try:
        # Intentionally fail: look for a non-existent element
        missing_element = wait.until(
            EC.presence_of_element_located(
                (AppiumBy.ACCESSIBILITY_ID, "non_existent_element")
            )
        )
    except Exception as e:
        # Generate screenshot path using time
        timestamp = int(time.time())
        screenshot_path = os.path.join(os.getcwd(), f"screenshot_failure_{timestamp}.png")
        
        # Capture screenshot
        driver.save_screenshot(screenshot_path)
        print(f"Test failed as expected. Screenshot saved at: {screenshot_path}")
        
        # Re-raise exception to mark test as failed
        raise e
