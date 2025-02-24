# Property Processing Scripts

This repository contains three scripts:

1. **Helper Script (`helper.py`)** - Fetches property details from an API and updates `todaysProperties.csv`.
2. **Main Script (`script.py`)** - Reads `todaysProperties.csv`, processes properties, and triggers an API request.
3. **Configuration File (`config.py`)** - Stores API URL, Bearer token, and file paths for easy configuration.

## Prerequisites

Ensure you have the following installed:

- Python 3.x
- Required dependencies (install using `pip install -r requirements.txt`)

## Configuration

Update `config.py` with the required settings:

```python
API_URL = "http://127.0.0.1:5000/api"
BEARER_TOKEN = "test_mock_token"
CSV_FILE_PATH = "todaysProperties.csv"
```

## Running the Mock Server (For Testing)

To test the full flow without affecting production, use the mock API server included in `server.py`. Start the server before executing the scripts:

```sh
python server.py
```

## Running the Scripts for Testing

1. **Run the Helper Script** - Fetches active properties and updates the CSV file:
   ```sh
   python helper.py
   ```
2. **Run the Main Script** - Processes properties and triggers the API request:
   ```sh
   python script.py
   ```

If testing is successful and you want to switch to production, update `config.py` with the correct API URL and Bearer token.

## CSV File Format

### Input Format (Before `helper.py` runs):

```
PropertyId
2
3
4
```

### Output Format (After `helper.py` runs):

```
PropertyCode,PropertyID
IDKA,23
OFKS,9
UFHL,3
```

## API Endpoints (Mock Server)

1. **Fetch Properties:** `GET /api/feedConfigurations`
2. **Trigger Property Jobs:** `PUT /api/pmsStayRaw/unsetEmptyOrNullFields`

## Notes

- The mock server simulates API behavior.
- Update `config.py` to use a real API in production.
- Ensure `todaysProperties.csv` is correctly formatted before running `script.py`.

## Troubleshooting

- If the API request fails with `400`, ensure the server is running and configured correctly.
- If no properties are updated, check that the helper script is filtering correctly.
- If authentication fails, verify the Bearer token in `config.py`.

For any issues, feel free to raise an issue in the repository!

---

Happy coding! 🚀
