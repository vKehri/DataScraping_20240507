from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd

# Specify the path to chromedriver if it's not in your PATH
chrome_path = r"C:\chromedriver-win64\chromedriver.exe"

# Set up Selenium WebDriver
service = Service(executable_path=chrome_path)
driver = webdriver.Chrome(service=service)

# Function to scrape data from a given URL


def scrape_data(url):
    try:
        driver.get(url)
        driver.implicitly_wait(10)  # Adjust the wait time as needed

        # Find the table using its XPath
        table = driver.find_element(
            By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/div/div/div[3]/div/section[1]/div[2]/table')

        # Extract data from the table
        rows = table.find_elements(By.TAG_NAME, "tr")
        data = []
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            data.append([col.text for col in cols])

        # Convert the list of data into a pandas DataFrame
        df = pd.DataFrame(data[1:], columns=data[0])
        return df
    except Exception as e:
        print(f"Error processing {url}: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error


# Read URLs from a text file
with open('data/urls.txt', 'r') as file:
    urls = file.read().splitlines()

# Loop through each URL and process it
all_data = []

for url in urls:
    df = scrape_data(url)
    if not df.empty:
        print("DataFrame before transposition:")
        print(df)

        # Adjust this condition based on your actual needs
        if df.shape[0] > 1:
            # You can choose to process the DataFrame without transposing
            # For example, rename the first column to 'Attribute' and the second to 'Value'
            if len(df.columns) == 2:
                df.columns = ['Attribute', 'Value']
                all_data.append(df)
            else:
                print("Unexpected number of columns in DataFrame for URL:", url)
        else:
            print("DataFrame from URL:", url,
                  "does not meet the processing criteria.")
    else:
        print("No data found for URL:", url)

# Only attempt to concatenate if all_data is not empty
if all_data:
    combined_data = pd.concat(all_data, ignore_index=True)
    print("Combined DataFrames:")
    print(combined_data)
else:
    print("No suitable data was collected from the URLs provided.")

# Close the browser
driver.quit()
