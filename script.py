import csv
import requests
import pyperclip
import sys
import config

API_URL = f'{config.API_URL}/pmsStayRaw/unsetEmptyOrNullFields'
BEARER_TOKEN = config.BEARER_TOKEN
CSV_FILE_PATH = config.CSV_FILE_PATH
MAX_REQUESTS = 10

def send_request(property_id, property_code):
    try:
        response_obj = requests.put(
            f"{API_URL}?propertyIds={property_id}",
            headers={
                'Authorization': f'Bearer {BEARER_TOKEN}',
                'Content-Type': 'application/json'
            }
        )
        
        if response_obj.status_code != 200:
            print(f"API request failed with status: {response_obj.status_code}")
            sys.exit(1)
        
        data = response_obj.json()
        if data.get('result', {}).get('success') and data.get('result', {}).get('message') == "Jobs started successfully":
            print(f"Response for Property ID {property_id}:", data)
            pyperclip.copy(property_code.strip())
            return True
        else:
            print(f"Unexpected API response: {data}")
            sys.exit(1)
    except Exception as error:
        print(f"Error sending request for Property ID {property_id}: {error}")
        sys.exit(1)

def process_csv():
    try:
        while True:
            with open(CSV_FILE_PATH, newline='', encoding='utf-8-sig') as csvfile:
                reader = list(csv.reader(csvfile))
                if len(reader) <= 1:  # Ensure at least one data row exists
                    print("CSV file is empty or contains only headers. Exiting.")
                    sys.exit()
                
                # Skip header row
                row = reader[1]
                if len(row) < 2:
                    continue
                
                property_code, property_id = row[0], row[1]
                input(f"Press Enter to send request for Property Code: {property_code} with Property ID: {property_id}...")
                if send_request(property_id, property_code):
                    reader.pop(1)  # Remove the processed row, keeping headers
                    with open(CSV_FILE_PATH, 'w', newline='', encoding='utf-8-sig') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerows(reader)
    except Exception as e:
        print(f"Error processing CSV file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    process_csv()
