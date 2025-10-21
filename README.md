# Ampere

A Python client library for fetching data from the Ampere.IQ energy management system by Energiekonzepte Deutschland.

> **Note:** This library was generated with AI assistance but designed and reviewed by a human.

## Installation

```bash
pip install -e .
```

Or install from requirements:

```bash
pip install -r requirements.txt
```

## Usage

```python
from ampere import AmpereClient

# Initialize the client with your Ampere.IQ system URL
client = AmpereClient('https://your-ampere-system.local')

# Authenticate
client.login('your-password')

# Fetch energy overview data
overview = client.energy_overview()
print(overview.production)
print(overview.consumption)
```

## API Reference

### `AmpereClient(base_url)`

Initialize a new Ampere.IQ API client.

**Parameters:**
- `base_url` (str): Base URL of your Ampere.IQ system

### Methods

#### `login(password)`
Authenticate with the Ampere.IQ system.

**Parameters:**
- `password` (str): The installer password

**Raises:**
- `requests.exceptions.HTTPError`: If authentication fails

#### `energy_overview()`
Fetch current energy overview data from the system.

**Returns:**
- `SimpleNamespace`: Energy data with attribute access (e.g., `production`, `consumption`)

**Raises:**
- `requests.exceptions.RequestException`: If the request fails

## License

MIT
