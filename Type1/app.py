from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
from flask import Flask, render_template, jsonify
from datetime import datetime
import uuid
import requests
from dotenv import TWITTER_USER,TWITTER_PASS,PROXYMESH_URL,PROXY_USERNAME,PROXY_PASSWORD,MongoUrl

# MongoDB setup
client = MongoClient("")
db = client.trending_topics
collection = db.trends

# Flask setup
app = Flask(__name__)

seleniumwire_options = {
    'proxy': {
        'http': f'http://{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXYMESH_URL}',
        'https': f'http://{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXYMESH_URL}',
    }
}

def fetch_trending_topics():
    
    # Seleniumwire setup
    unique_id = str(uuid.uuid4())
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options)
    
    try:
        # Twitter login page
        driver.get("https://x.com/i/flow/login?lang=en")
        
        # Enter user_id
        WebDriverWait(driver, 1000).until(
            EC.presence_of_element_located((By.NAME, "text"))
        ).send_keys((TWITTER_USER) + Keys.RETURN)
        
        # Enter pass
        WebDriverWait(driver, 1000).until(
            EC.presence_of_element_located((By.NAME, "password"))
        ).send_keys((TWITTER_PASS) + Keys.RETURN)
        
        WebDriverWait(driver, 1000).until(
            EC.presence_of_element_located((By.XPATH, f'//div[@aria-label="Timeline: Trending now"]/div/div[3]/div/div/div/div[2]'))
        )
        
        # Scraping trends from "What's happening section"
        trending_topic_content=[]
        for i in range(3,7):
            xpath = f'//div[@aria-label="Timeline: Trending now"]/div/div[{i}]/div/div/div/div[2]'
            trending_topic = driver.find_element(By.XPATH, xpath)
            trending_topic_content.append(trending_topic.text)
            
        # Get ip address
        ip_address = requests.get("http://ipinfo.io/ip").text.strip()
        
        # Save to MongoDB
        record = {
            "_id": unique_id,
            "trend1": trending_topic_content[0],
            "trend2": trending_topic_content[1],
            "trend3": trending_topic_content[2],
            "trend4": trending_topic_content[3],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "ip_address": ip_address,
        }
        collection.insert_one(record)
        return record
    
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        driver.quit()

@app.route("/run-script", methods=["GET"])
def run_script():
    record = fetch_trending_topics()
    return jsonify(record)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)