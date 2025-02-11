import json
from selenium import webdriver
import schedule
import time

# Function to fetch data
def get_data():
    # Initialize the browser
    browser = webdriver.Firefox()

    # Fetch the webpage
    url = 'https://kick.com/api/v2/channels/25616466/messages'
    browser.get(url)

    # Get the page source
    page_source = browser.page_source

    # Remove the HTML tags
    json_data = page_source.replace("<html><head></head><body>", "").replace("</body></html>", "")

    # Parse the JSON string to ensure it's valid
    parsed_data = json.loads(json_data)

    # Save the JSON data to a file
    output_file = "C:/Users/eng/Desktop/selenyum/messages.json"
    with open(output_file, "a", encoding="utf-8") as file:
        json.dump(parsed_data, file, ensure_ascii=False, indent=4)

    # Print confirmation
    print(f"JSON data saved to {output_file}")
    
    # Close the browser
    browser.quit()

# Schedule the function to run every 5 minutes
schedule.every(0.12).minutes.do(get_data)

print("Scheduler started. Press Ctrl+C to stop.")

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
