import logging
from scraper import scrape_olx_audi_data
from data_processing import save_to_csv
import config  # Import the config module

def main():
    """
    Main function to run the scraper and save the data.
    Uses configuration from config.py.
    """
    # Scrape the car data from the URL specified in config
    car_data = scrape_olx_audi_data(config.SCRAPE_URL)
    
    # Check if any data was scraped
    if car_data:
        # If data was scraped, save it to the CSV file specified in config
        save_to_csv(car_data, config.OUTPUT_FILE)
        print(f"Data saved to {config.OUTPUT_FILE}")
    else:
        # If no data was scraped, print a message
        print("No data to save.")

if __name__ == "__main__":
    # Set up basic configuration for logging using settings from config
    logging.basicConfig(level=config.LOG_LEVEL, format=config.LOG_FORMAT)
    
    # Run the main function
    main()