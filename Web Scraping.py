from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import collections
import time

# Specify the path to the ChromeDriver executable
path = "C:\\Users\\ayush\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"

# Set the options for the Chrome WebDriver
options = webdriver.ChromeOptions()
options.binary_location = path

# Initialize the Chrome WebDriver with the options
driver = webdriver.Chrome(options=options)

# Open the specified website
website = 'https://www.dailymotion.com/tseries2'
driver.get(website)

# You can add some interactions here if needed
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


# Don't forget to close the driver when done
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