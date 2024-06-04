# Dailymotion T-Series Video Scraper

This project uses Selenium to scrape the first 500 video URLs uploaded by T-Series on the Dailymotion website. It then extracts the video IDs from these URLs and finds the most frequently repeated character in the video IDs.

## Requirements

- Python 3.7+
- Selenium
- WebDriver Manager for Selenium

## Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/your-username/dailymotion-tseries-scraper.git
    cd dailymotion-tseries-scraper
    ```

2. **Install required Python packages:**
    ```sh
    pip install selenium
    pip install webdriver-manager
    ```

3. **Download ChromeDriver:**
    - Ensure you have the Chrome browser installed.
    - Download the ChromeDriver that matches your Chrome version from [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads).
    - Extract the downloaded file and note the path to `chromedriver.exe`.

## Usage

1. **Modify the paths in the script:**
    - Open `scraper.py` and update the following variables with the correct paths:
      ```python
      chrome_driver_path = "C:\\Path\\To\\Your\\chromedriver.exe"
      chrome_binary_path = "C:\\Path\\To\\Your\\chrome.exe"
      ```

2. **Run the script:**
    ```sh
    python scraper.py
    ```

3. **Output:**
    - The script will print the most frequently repeated character in the video IDs and its count.

## Code Explanation

### scraper.py

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import collections
import time

# Path to the ChromeDriver executable
chrome_driver_path = "C:\\Users\\ayush\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"

# Path to the Chrome executable
chrome_binary_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

# Set the options for the Chrome WebDriver
options = webdriver.ChromeOptions()
options.binary_location = chrome_binary_path
options.headless = True  # Run in headless mode
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Initialize the Chrome WebDriver with the correct executable path
driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

# Open the specified website
website = 'https://www.dailymotion.com/tseries2'
driver.get(website)

# Collect video URLs
video_urls = set()  # Use a set to avoid duplicates
while len(video_urls) < 500:
    # Find all video elements on the page
    video_elements = driver.find_elements(By.XPATH, "//a[contains(@href, '/video/')]")
    for video in video_elements:
        href = video.get_attribute('href')
        if href and href.startswith('https://www.dailymotion.com/video/') and href not in video_urls:
            video_urls.add(href)
        if len(video_urls) >= 500:
            break
    
    # Scroll down to load more videos
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

# Close the browser
driver.quit()

# Extract video IDs from the URLs
video_ids = [url.split('/video/')[1] for url in list(video_urls)[:500]]

# Count the frequency of each character in the video IDs
char_counter = collections.Counter(''.join(video_ids))

# Find the most frequently repeated character
most_common_char, most_common_count = None, 0
for char in sorted(char_counter.keys()):  # sorted to handle alphabetic order in case of tie
    if char_counter[char] > most_common_count:
        most_common_char, most_common_count = char, char_counter[char]

# Print the result
print(f"{most_common_char}:{most_common_count}")
