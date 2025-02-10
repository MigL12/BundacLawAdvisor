from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# Setup WebDriver with ChromeDriver path
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.implicitly_wait(5)  # Default wait time for all elements


def test_standard_user_checkout():
    """Test Scenario 1"""
    
    # Open the website
    driver.get("https://www.saucedemo.com/")
    time.sleep(1)  # Slowing down to see page load

    # Login as standard_user
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(1)  #  login 

    # Add items to cart
    driver.find_element(By.ID, "add-to-cart-sauce-labs-bolt-t-shirt").click()
    driver.find_element(By.ID, "add-to-cart-sauce-labs-fleece-jacket").click()
    time.sleep(1)  # Ensure items are added

    # Click cart and verify items
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    time.sleep(1)  # Slow down to see cart

    assert "Sauce Labs Bolt T-Shirt" in driver.page_source
    assert "Sauce Labs Fleece Jacket" in driver.page_source

    # Checkout process
    driver.find_element(By.ID, "checkout").click()
    time.sleep(1)  # Checkout screen

    driver.find_element(By.ID, "first-name").send_keys("John")
    driver.find_element(By.ID, "last-name").send_keys("Doe")
    driver.find_element(By.ID, "postal-code").send_keys("12345")
   

    driver.find_element(By.ID, "continue").click()
    time.sleep(1)  # Order summary

    # Verify total price is displayed
    total_price = driver.find_element(By.CLASS_NAME, "summary_total_label").text
    assert "Total" in total_price
    time.sleep(1)

    # Complete the purchase
    driver.find_element(By.ID, "finish").click()
    time.sleep(1)  # Confirmation page

    # Verify order completion message
    success_message = driver.find_element(By.CLASS_NAME, "complete-header").text
    assert success_message == "Thank you for your order!"

    print(" Scenario 1 Passed!")


def test_locked_out_user_login():
    """Test Scenario 2"""

    # Open the website
    driver.get("https://www.saucedemo.com/")
    time.sleep(1)  

    # Login as locked_out_user
    driver.find_element(By.ID, "user-name").send_keys("locked_out_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(1)  # Wait for error message to appear


    error_message = driver.find_element(By.CLASS_NAME, "error-message-container").text
    assert "Epic sadface: Sorry, this user has been locked out" in error_message

    print("Scenario 2 Passed!")


test_standard_user_checkout()
test_locked_out_user_login()

time.sleep(10)
driver.quit()
