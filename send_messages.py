import time
import pandas as pd
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# === Load Template ===
with open("template.txt", "r", encoding="utf-8") as f:
    MESSAGE_TEMPLATE = f.read()

def fill_template(row):
    return MESSAGE_TEMPLATE.format(
        name=row.get("name", ""),
        phone=row.get("phone", ""),
        day=row.get("day", ""),
        hour=row.get("hour", ""),
        location=row.get("location", ""),
        instrument=row.get("instrument", ""),
    )

# === Config ===
CSV_FILE = "contacts.csv"
DELAY_BETWEEN_MSGS = 5  # seconds

# === Load contacts ===
df = pd.read_csv(CSV_FILE)

# === Start WhatsApp Web ===
options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=./User_Data")  # keep login session
driver = webdriver.Chrome(options=options)

# === Send Messages ===schedule_
for _, row in df.iterrows():
    message = fill_template(row)
    encoded_msg = urllib.parse.quote(message)
    phone = str(row["phone"])

    url = f"https://web.whatsapp.com/send?phone={phone}&text={encoded_msg}"
    driver.get(url)

    try:
        # ✅ Wait until message input box is available
        msg_box = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
        )
        # Press ENTER to send
        msg_box.send_keys(Keys.ENTER)
        print(f"✅ Sent to {row['name']} ({phone})")
    except Exception as e:
        print(f"❌ Failed for {row['name']} ({phone}): {e}")

    time.sleep(DELAY_BETWEEN_MSGS)

print("🎉 All messages sent!")
driver.quit()
