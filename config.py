# URL to scrape Audi cars from OLX
SCRAPE_URL = "https://www.olx.pt/carros-motos-e-barcos/carros/audi/"

# Output file name for the CSV
OUTPUT_FILE = "audi_cars.csv"

# Logging configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

# Selenium WebDriver settings
WEBDRIVER_WAIT_TIME = 10  # seconds
PAGE_LOAD_WAIT_TIME = 5  # seconds

# CSV field names
CSV_FIELDS = ['Brand', 'Model', 'Year', 'Price', 'Kilometers']