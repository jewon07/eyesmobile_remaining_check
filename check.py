from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.common.by import By
import time
import requests
import schedule

def check_remaining_sayongryang():

    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    service = Service(excutable_path=ChromeDriverManager().install()) 
    driver = webdriver.Chrome(service=service, options = chrome_options)

    driver.get("https://www.eyes.co.kr/")
    driver.maximize_window()
    time.sleep(1)

# 이벤트 광고창 닫기
    driver.find_element(By.XPATH, '/html/body/div[4]/div/button').click()
    time.sleep(1)
# 로긴버튼 클릭
    driver.find_element(By.XPATH, '//*[@id="wrap"]/header/div[1]/div[2]/div/a[2]').click()
# 아이디
    id = driver.find_element(By.XPATH, '//*[@id="login_id"]')
    id.click()
    id.send_keys('아이디')

# 비번
    pw = driver.find_element(By.XPATH, '//*[@id="login_pw"]')
    pw.click()
    pw.send_keys('비번')

    driver.find_element(By.XPATH, '//*[@id="loginBtn"]').click()
    time.sleep(3)

# 이벤트 광고창 닫기
    driver.find_element(By.XPATH, '/html/body/div[4]/div/button/span').click()
    time.sleep(1)

# 마이페이지 입갤
    driver.find_element(By.XPATH, '//*[@id="wrap"]/header/div[1]/div[2]/div/a[1]').click()
    time.sleep(1)

#사용량 입갤
    driver.find_element(By.XPATH, '//*[@id="wrap"]/main/div[2]/div[2]/div[7]/div[2]/div[1]/button').click()
    time.sleep(1)

    moonja = driver.find_element(By.XPATH, '//*[@id="smsChange1"]')
    data = driver.find_element(By.XPATH, '//*[@id="dataChange1"]')
    tonghwa = driver.find_element(By.XPATH, '//*[@id="voiceChange1"]')

    def send_telegram_message(message):
        token = '봇 토큰'
        chat_id = '채널 id'
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': f'남은 문자 : {moonja.text}\n남은 데이터 :{data.text}\n남은 통화 : {tonghwa.text}'
        }
        response = requests.post(url, data=payload)
        return response.json()
    send_telegram_message("사용량 보고")

schedule.every().day.at("22:00").do(check_remaining_sayongryang)

while True:
    schedule.run_pending()
    time.sleep(1)