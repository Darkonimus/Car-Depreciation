import csv
import logging
from typing import List, Dict, Any
import config  # Add this import

def save_to_csv(car_data: List[Dict[str, Any]], filename: str):
    """
    Save the scraped car data to a CSV file.
    Uses field names from config.py.
    
    Args:
    car_data (List[Dict[str, Any]]): A list of dictionaries containing car information.
    filename (str): The name of the file to save the data to.
    """
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        # Use field names from config
        writer = csv.DictWriter(csvfile, fieldnames=config.CSV_FIELDS)
        writer.writeheader()
        for car in car_data:
            writer.writerow(car)
    
    logging.info(f"Data saved to {filename}")