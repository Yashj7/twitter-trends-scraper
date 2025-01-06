# Twitter Trending Topics Scraper

This project is a Flask-based web application designed to scrape trending topics from Twitter (now X) using Selenium, ProxyMesh, and MongoDB. The app runs in headless Chrome and utilizes Selenium Wire to handle proxy authentication, allowing anonymous browsing. The primary function of the app is to scrape the top trending topics and store them in a MongoDB database along with relevant metadata like timestamp and IP address.
Features:

  1. Proxy Authentication: The app uses ProxyMesh to scrape Twitter anonymously by configuring a proxy.
  2. MongoDB Storage: The scraped trending topics, along with timestamp and IP address, are saved into a MongoDB database for easy retrieval and analysis.
  3. Selenium & Headless Chrome: The app uses Selenium to interact with the Twitter interface and fetch data from the "home page" or "Search and Explore" section in a headless Chrome browser.
  4. Flask Web Application: A Flask-based API to trigger the scraping process and return the results as a JSON response.

# How the App Works:

1. Login to Twitter (X):

The app automates the login process using Selenium, where the credentials for Twitter are entered, and it waits for the login to be successful before moving on to scrape trends.

2. Scraping Trends:

  Type 1: Scrapes the top 4 trending topics from the home page of Twitter (only visible trends).
  
  Type 2: Scrapes the top 5 trending topics from the "Search and Explore" panel, where more detailed trends are displayed.

3. Proxy Management:

  The app uses ProxyMesh to route the traffic through a proxy, making the scraping process more anonymous. The app handles proxy authentication with a username and password.

4. Storing Data in MongoDB:

Once the trends are scraped, the app saves the data, along with the timestamp and the proxy's IP address (retrieved using an external API), into MongoDB. This allows you to track the trends over time and associate each scrape with the IP address used for the proxy.

5. API Endpoints:

   /run-script: Triggers the scraping process and returns the scraped data as a JSON response, including the trending topics, timestamp, and IP address.

   /: Displays the home page of the app (can be customized with any front-end features or information you want to provide).

Technologies Used:

  1. Python: The programming language used to write the app.
  
  2. Flask: A lightweight web framework used to create the app’s API.
  
  3. Selenium: Web automation tool for interacting with Twitter's web interface.
  
  4. ProxyMesh: A proxy service used to ensure anonymous scraping.
  
  5. MongoDB: NoSQL database to store the scraped trending topics.
  
  6. Chrome WebDriver: To drive the browser in headless mode, scraping the data.
  
  7. Requests: Used to fetch the IP address of the proxy.

Setup Instructions:

1. Clone the Repository:

       git clone https://github.com/yashj7/twitter-trends-scraper.git
       cd twitter-trends-scraper

3. Install Dependencies:

  Make sure you have Python installed, and then install the required dependencies:

    pip install -r requirements.txt

3. Set up MongoDB:

  You need a MongoDB cluster or a local MongoDB server to store the data. Set up MongoDB and connect it by editing the MongoDB connection URI in the code.

4. Set up Proxy Details:

  Make sure to configure the ProxyMesh credentials in the code with your own username and password.
  
5. Run the Application:

  python app.py

  The app will start running locally, and you can access it at http://127.0.0.1:5000.
  
API Endpoints:
  
  1. GET /run-script

  Triggers the scraping process and returns the scraped trending topics, timestamp, and proxy IP as a JSON response.

  Example Response:

{
    "_id": "unique-id",
    "trend1": "Trend Topic 1",
    "trend2": "Trend Topic 2",
    "trend3": "Trend Topic 3",
    "trend4": "Trend Topic 4",
    "timestamp": "2025-01-06 12:34:56",
    "ip_address": "192.168.1.1"
}

2. GET /

  Serves the home page of the app (can be customized with a front-end template).
