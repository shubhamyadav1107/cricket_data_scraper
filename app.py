from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import schedule
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Function to initialize the Selenium WebDriver
def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run headlessly (without opening a browser window)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

# Function to fetch the match schedule using Selenium
def fetch_schedule():
    base_url = "https://crex.live"
    url = f"{base_url}/fixtures/match-list"
    
    # Initialize WebDriver
    driver = get_driver()
    
    try:
        # Open the webpage
        driver.get(url)
        
        # Wait for the match data to be loaded dynamically (adjust the waiting time if needed)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h3.match-info"))  # Wait for match data to load
        )
        
        # Get the page source after JavaScript execution
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Find all h3 elements with class "match-info"
        matches = soup.find_all('h3', class_='match-info')
        
        match_data = []
        for match in matches:
            # Extract the text from the match details
            match_info = match.get_text(strip=True)
            match_data.append({
                'title': match_info
            })
        
        return match_data
    
    finally:
        # Close the browser
        driver.quit()

# Function to monitor matches at regular intervals
def monitor_matches():
    print("Monitoring matches...")
    match_data = fetch_schedule()
    print("Match data fetched:", match_data)
    # You can add logic to trigger further scraping for details like scorecard here

# Schedule the task to run periodically (every 10 minutes in this case)
schedule.every(10).minutes.do(monitor_matches)

# Main program loop
if __name__ == "__main__":
    print("Starting real-time cricket data scraping system...")
    
    # Run the scheduled task
    while True:
        schedule.run_pending()
        time.sleep(1)  # Check for pending tasks every second
