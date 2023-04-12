from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scrape import main
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

app = FastAPI()
url = 'https://www.google.com/maps/'



origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('--blink-settings=imagesEnabled=false')
driver = webdriver.Chrome(options=options)
driver.get(url)
try:
		cookiesDecliner = WebDriverWait(driver, timeout=1).until(lambda b: b.find_element(By.XPATH,"//button[@class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 Nc7WLe']"))
		cookiesDecliner.click()
except:
		pass
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/rushhours/{query}/{amount}")
async def getRushhours(query: str, amount: int):
    print(query, amount)
    data = main(driver, query, amount)
    return {'data': data}