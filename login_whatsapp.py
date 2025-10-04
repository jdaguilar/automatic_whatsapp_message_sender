import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def login_whatsapp():
    options = webdriver.ChromeOptions()
    options.add_argument("--user-data-dir=./User_Data")  # persistent session
    driver = webdriver.Chrome(options=options)
    driver.get("https://web.whatsapp.com/")
    print("📱 Scan the QR code if needed...")

    try:
        # Wait until search bar appears (means you’re logged in)
        WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
        )
        print("✅ WhatsApp Web login successful!")
    except Exception:
        print("❌ Login failed or timed out.")
    finally:
        # Keep browser open to maintain session
        print("⚡ Do not close this browser if you want to reuse the session.")
        while True:
            time.sleep(60)  # Keep session alive

if __name__ == "__main__":
    login_whatsapp()
