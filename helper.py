import csv
import requests
import sys
import config

# Build the API URL for fetching property details.
# Here, we assume the endpoint returns all property objects without requiring query parameters.
API_URL = f'{config.API_URL}/feedConfigurations'
BEARER_TOKEN = config.BEARER_TOKEN
CSV_FILE_PATH = config.CSV_FILE_PATH

def fetch_all_properties():
    """Fetch all property details from the API in one call (without query parameters)."""
    try:
        response = requests.get(
            API_URL,
            headers={'Authorization': f'Bearer {BEARER_TOKEN}'}
        )
        if response.status_code != 200:
            print(f"API request failed with status: {response.status_code}")
            return None
        data = response.json()
        if 'result' in data:
            return data['result']
        return None
    except Exception as e:
        print(f"Error fetching properties: {e}")
        return None

def process_csv():
    """
    Read property IDs from CSV (old format with header 'PropertyId'),
    fetch all property details in a single API call, filter by:
      - status == "ACTIVE"
      - incomingSystem == "MARS"
    and then update the CSV to the new format:
      PropertyCode,PropertyID
    """
    try:
        # Read the CSV and its header
        with open(CSV_FILE_PATH, newline='', encoding='utf-8-sig') as csvfile:
            reader = list(csv.reader(csvfile))
            if len(reader) <= 1:
                print("CSV file is empty or contains only headers. Exiting.")
                sys.exit()

            header = reader[0]
            # Check header to determine format
            if header[0].strip().lower() == "propertyid":
                # Old format: single column of property IDs
                property_ids = {row[0].strip() for row in reader[1:] if row and row[0].strip()}
            elif header[0].strip().lower() == "propertycode":
                print("CSV file is already in the new format. Exiting without changes.")
                sys.exit(0)
            else:
                print("CSV file header does not match expected structure. Exiting.")
                sys.exit(1)

        # Fetch all property details with one API call
        all_properties = fetch_all_properties()
        if all_properties is None:
            print("Failed to fetch property details.")
            sys.exit(1)

        updated_rows = [["PropertyCode", "PropertyID"]]  # New CSV header

        # Filter properties: only include those that:
        # 1. Have a propertyId present in the CSV.
        # 2. Meet the conditions: status == "ACTIVE" and incomingSystem == "MARS".
        for prop in all_properties:
            prop_id = str(prop.get("propertyId"))
            if prop_id in property_ids:
                if (prop.get("status") == "ACTIVE" and 
                    prop.get("incomingSystem") == "MARS"):
                    updated_rows.append([prop.get("propertyCode"), prop_id])

        if len(updated_rows) == 1:
            print("No matching properties found. CSV file remains unchanged.")
            sys.exit(0)

        # Write the updated CSV, preserving the new structure.
        with open(CSV_FILE_PATH, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(updated_rows)

        print("Updated CSV successfully!")

    except Exception as e:
        print(f"Error processing CSV: {e}")
        sys.exit(1)

if __name__ == "__main__":
    process_csv()
