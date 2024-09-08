# Import necessary libraries
import config
import requests  # For making HTTP requests
from bs4 import BeautifulSoup  # For parsing HTML content
import re  # For regular expressions
from selenium import webdriver  # For browser automation
from selenium.webdriver.chrome.service import Service  # For configuring the ChromeDriver service
from selenium.webdriver.chrome.options import Options  # For setting Chrome options
from selenium.webdriver.common.by import By  # For locating elements on web pages
from selenium.webdriver.support.ui import WebDriverWait  # For waiting for page elements to load
from selenium.webdriver.support import expected_conditions as EC  # For specifying expected conditions in WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager  # For managing ChromeDriver installation
import time  # For adding delays
from selenium.common.exceptions import NoSuchElementException  # For handling element not found exceptions

def is_url_scrapable(url):
    """
    Check if a given URL is accessible and can be scraped.
    
    Args:
    url (str): The URL to check.
    
    Returns:
    bool: True if the URL is accessible, False otherwise.
    """
    try:
        # Attempt to send a GET request to the URL
        response = requests.get(url)
        # Return True if the status code is 200 (OK)
        return response.status_code == 200
    except:
        # Return False if any exception occurs (e.g., network error)
        return False

def extract_year_and_km(text):
    """
    Extract year and kilometer information from a given text.
    
    Args:
    text (str): The text to extract information from.
    
    Returns:
    tuple: A tuple containing the extracted year and kilometers.
    """
    year = "N/A"
    kilometers = "N/A"
    
    # Use regex to find a year between 1900 and 2099
    year_match = re.search(r'\b(19|20)\d{2}\b', text)
    if year_match:
        year = year_match.group()
    
    # Use regex to find kilometer information
    km_match = re.search(r'(\d{1,3}(?:\.\d{3})*|\d+)\s*(?:mil\s*)?km', text, re.IGNORECASE)
    if km_match:
        kilometers = km_match.group(1).replace('.', '').replace(',', '')
    
    return year, kilometers

def clean_model(model: str) -> str:
    """
    Clean the model name by removing unwanted text and formatting.
    
    Args:
    model (str): The model name to clean.
    
    Returns:
    str: The cleaned model name.
    """
    # Remove text within parentheses, square brackets, or quotes
    model = re.sub(r'\([^)]*\)', '', model)
    model = re.sub(r'\[[^]]*\]', '', model)
    model = re.sub(r'"[^"]*"', '', model)
    model = re.sub(r"'[^']*'", '', model)
    
    # List of unwanted phrases to remove
    unwanted_phrases = [
        "aceito trocas", "muito estimado", "Aceita-se Retoma", "Negociavel",
        "Venda de Carro Usado em Excelente Estado!", "nacional estimado troco",
        "ano", "c/Garantia", "Com alguma mecanica eletronica",
        "Desde", "FULL EXTRAS", "Unico Dono", "Vendido com garantia", "Vendo"
    ]
    # Remove each unwanted phrase from the model name
    for phrase in unwanted_phrases:
        model = model.replace(phrase, '')
    
    # Remove extra spaces and return the cleaned model name
    return ' '.join(model.split()).strip()

def clean_price(price):
    """
    Clean the price string by removing newlines and extra spaces.
    
    Args:
    price (str): The price string to clean.
    
    Returns:
    str: The cleaned price string.
    """
    if price == "N/A":
        return price
    # Take only the first line (removes "Negociável" if present)
    return price.split('\n')[0].strip()

def scrape_olx_audi_data(url):
    """
    Scrape Audi car data from the given OLX URL using Selenium.
    
    Args:
    url (str): The URL to scrape.
    
    Returns:
    list: A list of dictionaries containing scraped car data.
    """
    # Set up Chrome options for headless browsing
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    
    # Set up the Chrome driver with automatic version detection
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Navigate to the URL
        driver.get(url)
        
        # Wait for the car listings to load
        WebDriverWait(driver, config.WEBDRIVER_WAIT_TIME).until(
            EC.presence_of_element_located((By.CLASS_NAME, "css-1sw7q4x"))
        )
        
        # Give the page a moment to fully load
        time.sleep(5)

        # Find all car listings
        car_listings = driver.find_elements(By.CLASS_NAME, "css-1sw7q4x")
        print(f"Found {len(car_listings)} car listings")

        cars = []
        for index, listing in enumerate(car_listings, 1):
            try:
                print(f"\nProcessing listing {index}:")
                
                # Extract title
                title = listing.find_element(By.CLASS_NAME, "css-1wxaaza").text if listing.find_elements(By.CLASS_NAME, "css-1wxaaza") else "N/A"
                print(f"Title: {title}")

                # Extract and clean price
                price = clean_price(listing.find_element(By.CLASS_NAME, "css-13afqrm").text if listing.find_elements(By.CLASS_NAME, "css-13afqrm") else "N/A")
                print(f"Price: {price}")

                # Extract year and kilometers
                year, kilometers = "N/A", "N/A"
                year_km_element = listing.find_elements(By.CLASS_NAME, "css-efx9z5")
                if year_km_element:
                    year, kilometers = extract_year_and_km(year_km_element[0].text)

                # If year is still N/A, try to extract from title
                if year == "N/A":
                    year, _ = extract_year_and_km(title)

                print(f"Year: {year}")
                print(f"Kilometers: {kilometers}")

                # Extract and clean model
                model = clean_model(title.replace("Audi", "").replace(year, "").strip())
                print(f"Model extracted: {model}")

                # Add the extracted data to the cars list
                cars.append({
                    'Brand': 'Audi',
                    'Model': model,
                    'Year': year,
                    'Price': price,
                    'Kilometers': kilometers
                })
            except Exception as e:
                print(f"Error processing listing {index}: {str(e)}")
                continue

        if not cars:
            print("No car listings were successfully processed.")
        else:
            print(f"Successfully processed {len(cars)} car listings.")
        
        return cars

    finally:
        # Always close the browser, even if an error occurs
        driver.quit()