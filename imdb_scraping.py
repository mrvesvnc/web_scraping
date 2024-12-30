from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd

chrome_options = Options()
# chrome_options.add_argument("--headless")  # Headless mod
chrome_options.add_argument("--disable-gpu")  # Windows'ta GPU ile ilgili sorunları önler
chrome_options.add_argument("--no-sandbox")  # Bazı sistemlerde stabil çalışması için
chrome_options.add_argument("--disable-dev-shm-usage")  # Paylaşılan belleği devre dışı bırakır

driver = webdriver.Chrome(options=chrome_options)

# IMDB URL'sini aç
url = "https://www.imdb.com/title/tt1099212/reviews/"
driver.get(url)

# Yorumlar yüklenene kadar bekle
time.sleep(3)

# Düğmeyi seç ve tıkla
try:
    decline_button = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="reject-button"]')
    decline_button.click()
    print("Decline butonuna başarıyla tıklandı.")
except Exception as e:
    print(f"Decline butonuna tıklama başarısız: {e}")

# Sayfanın sonuna kaydır ve "All" butonuna tıkla

# Sayfanın toplam yüksekliğini alın
total_height = driver.execute_script("return document.body.scrollHeight")

driver.execute_script("window.scrollTo(0, 0);")

# Sayfayı sona yakın bir noktaya kaydırın (örneğin, %90'ına kadar)
scroll_position = total_height * 0.85  # Toplam yüksekliğin %90'ı
driver.execute_script(f"window.scrollTo(0, {scroll_position});")
time.sleep(2)  # Kaydırma sonrası bekleme

all_button = driver.find_element(By.XPATH, "//span[contains(@class, 'ipc-see-more sc-32dca5b4-0 exNxuq chained-see-more-button sc-f09bd1f5-2')]/button[contains(@class, 'ipc-btn ipc-btn--single-padding ipc-btn--center-align-content ipc-btn--default-height ipc-btn--core-base ipc-btn--theme-base ipc-btn--button-radius ipc-btn--on-accent2 ipc-text-button ipc-see-more__button')]")
all_button.click()
time.sleep(3)  # Sayfanın yüklenmesi için bekleme
print("All button clicked")

time.sleep(2)

# Tüm yorumları seç (spoiler'lı ve spoiler'sız dahil)
reviews = driver.find_elements(By.XPATH, '//div[@data-testid="review-overflow"] | //div[@class="ipc-html-content-inner-div"]')
comments = [review.text for review in reviews]

# Çekilen yorumları yazdırma
for i, comment in enumerate(comments, 1):
    print(f"Comment {i}: {comment}")

df = pd.DataFrame(comments, columns=["Comment"])
df.to_excel("imdb_comments.xlsx", index=False)  
