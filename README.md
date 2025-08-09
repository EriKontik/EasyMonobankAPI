# MonoBank API Python Client

A simple, user-friendly Python client for interacting with the MonoBank API.  
Easily fetch account info, statements, and more, with clear output and robust error handling.

## Features

- Fetch currency rates, client info, account statements, and jars
- Pretty-print all data in a readable format
- Customizable output (choose which sections to display)
- Easy setup with environment variables

## Getting Started

### 1. Clone the Repository

```powershell
git clone <your-repo-url>
cd MonoAPI
```

### 2. Install Dependencies

Make sure you have Python 3.7+ installed.

```powershell
pip install requests python-dotenv
```

### 3. Set Up Your API Key

Create a `.env` file in the project root:

```
API_KEY=your_monobank_api_key_here
```

### 4. Run the Script

```powershell
python mono_bank_API.py
```

### 5. Example Usage

The script will fetch and print your MonoBank client info and recent transactions in a beautiful, readable format.

You can also use the `show_data` function in your own scripts:

```python
from mono_bank_API import show_data, get_client_info, API_KEY

data = get_client_info(API_KEY)
show_data(data)
```

## Customization

- To display only specific sections (e.g., only accounts or jars), modify the `show_data` function or use the advanced `get_mono_data` function.
- All output is formatted for clarity and ease of reading.

## Troubleshooting

- Ensure your API key is valid and active.
- If you see errors about missing environment variables, check your `.env` file.
- For network errors, verify your internet connection and MonoBank API status.

## Contributing

Pull requests and suggestions are welcome!  
Feel free to open issues for bugs or feature requests.

**TODO**

[x] - Implement the base functionality for an API requests 

[x] - Add all the possible uses for an API

[ ] - Create a guide on how to use this repo

[ ] - Make it as user friendly and carefree as possible

