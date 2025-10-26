# ios-appium-test-automation
An iOS automation test suite for Apple’s Backyard Birds app using Appium and Python.
This repository contains a basic iOS automation testing framework using **Appium** and **Python (pytest)**.  
It demonstrates automation testing for iOS sample apps such as **Apple's Backyard Birds**.

## Features
- Appium + Python test framework
- Supports iOS simulator/device
- Runs smoke, navigation, and functional tests

## Setup
### Prerequisites
- macOS with Xcode installed  
- Appium Server or Appium Inspector  
- Python 3.10+  
- iOS simulator or physical device  


### Installation
```bash
git clone https://github.com/Nidhimehta2610/ios-appium-test-automation.git
cd ios-appium-test-automation
pip install -r requirements.txt

## Test Summary

**Total Scenarios:** 20  

** Passed:** 16  
** Failed:** 1  
** Skipped / Not Executed:** 3  

### Failed Scenarios
| Scenario | Issue |
|----------|-------|
| F1 — Toggle Favorite | Appium doesn’t detect updated button attributes |

### Skipped / Not Executed Scenarios
| Scenario | Reason |
|----------|--------|
| N4 — Pull-to-refresh (if available) | Spinner not available |
| F6 — Sort or category switch (if present) | Sorting not available |
| F9 — Offline/low-connectivity placeholder (if the app fetches data) | Not feasible |
