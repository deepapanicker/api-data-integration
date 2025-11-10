# API Data Integration

A Python framework for integrating with REST APIs to extract, transform, and load data. Includes support for authentication, rate limiting, error handling, and data validation.

## 🎯 Features

- **REST API Integration**: Easy-to-use framework for API data extraction
- **Authentication Support**: OAuth2, API keys, Basic Auth
- **Rate Limiting**: Built-in rate limiting and retry logic
- **Error Handling**: Comprehensive error handling and logging
- **Data Validation**: Validate API responses before processing
- **Incremental Loading**: Support for incremental data extraction
- **Multiple Formats**: Support for JSON, XML, and CSV responses
- **Pagination Support**: Automatic handling of paginated APIs

## 📋 Prerequisites

- Python 3.8+
- pip

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/deepapanicker/api-data-integration.git
cd api-data-integration
```

### 2. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 📁 Project Structure

```
api-data-integration/
├── src/
│   ├── clients/           # API client implementations
│   │   ├── base_client.py
│   │   ├── rest_client.py
│   │   └── oauth_client.py
│   ├── extractors/        # Data extraction modules
│   │   ├── api_extractor.py
│   │   └── incremental_extractor.py
│   ├── transformers/      # Data transformation
│   │   └── response_transformer.py
│   ├── loaders/           # Data loading
│   │   └── database_loader.py
│   └── utils/             # Utilities
│       ├── rate_limiter.py
│       └── error_handler.py
├── config/                # Configuration files
│   └── api_config.yaml.example
├── examples/              # Example scripts
│   ├── basic_extraction.py
│   ├── incremental_sync.py
│   └── oauth_example.py
├── tests/                 # Unit tests
├── ARCHITECTURE.md        # Architecture diagram and flow
├── requirements.txt
└── README.md
```

## 🚀 Quick Start

### Basic API Extraction

```python
from src.clients.rest_client import RESTClient
from src.extractors.api_extractor import APIExtractor

# Initialize client
client = RESTClient(
    base_url='https://api.example.com',
    api_key='your-api-key'
)

# Extract data
extractor = APIExtractor(client)
data = extractor.extract(endpoint='/customers', params={'limit': 100})

# Process data
for record in data:
    print(record)
```

### Incremental Extraction

```python
from src.extractors.incremental_extractor import IncrementalExtractor

extractor = IncrementalExtractor(
    client=client,
    endpoint='/orders',
    timestamp_field='updated_at',
    last_sync_file='last_sync.json'
)

# Extract only new/updated records
new_data = extractor.extract_incremental()
```

### OAuth2 Authentication

```python
from src.clients.oauth_client import OAuthClient

client = OAuthClient(
    base_url='https://api.example.com',
    client_id='your-client-id',
    client_secret='your-client-secret',
    token_url='https://api.example.com/oauth/token'
)

data = client.get('/protected-endpoint')
```

## 🔧 Configuration

### API Configuration

Edit `config/api_config.yaml`:

```yaml
apis:
  example_api:
    base_url: https://api.example.com
    authentication:
      type: api_key
      header: X-API-Key
      value: ${API_KEY}
    rate_limit:
      requests_per_second: 10
    retry:
      max_retries: 3
      backoff_factor: 2
```

## 📊 Usage Examples

### Complete ETL Pipeline

```python
from src.clients.rest_client import RESTClient
from src.extractors.api_extractor import APIExtractor
from src.transformers.response_transformer import ResponseTransformer
from src.loaders.database_loader import DatabaseLoader

# 1. Extract
client = RESTClient(base_url='https://api.example.com', api_key='key')
extractor = APIExtractor(client)
raw_data = extractor.extract('/customers', pagination=True)

# 2. Transform
transformer = ResponseTransformer()
transformed_data = transformer.transform(
    raw_data,
    field_mapping={'customer_id': 'id', 'customer_name': 'name'}
)

# 3. Load
loader = DatabaseLoader(connection_string='postgresql://...')
result = loader.load(
    data=transformed_data,
    table_name='customers',
    load_mode='upsert',
    unique_key='id'
)
```

### Rate Limiting

```python
from src.utils.rate_limiter import RateLimiter

rate_limiter = RateLimiter(requests_per_second=10)

for endpoint in endpoints:
    rate_limiter.wait_if_needed()  # Respect rate limits
    data = extractor.extract(endpoint)
```

### Error Handling

```python
from src.utils.error_handler import ErrorHandler

error_handler = ErrorHandler(log_file='errors.log')

try:
    data = extractor.extract('/endpoint')
except Exception as e:
    error_info = error_handler.handle_error(e, context={'endpoint': '/endpoint'})
    # Error logged and tracked
```

## 🏗️ Architecture

- **Architecture Details**: See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed architecture diagrams and data flow
- **Visual Diagrams**: See [DIAGRAM.md](DIAGRAM.md) for comprehensive visual diagrams showing system components and data flow

## 📝 Examples

### Run Examples

```bash
# Basic extraction
python examples/basic_extraction.py

# Incremental sync
python examples/incremental_sync.py

# OAuth2 example
python examples/oauth_example.py
```

## 🧪 Testing

```bash
pytest tests/
```

## 📚 Documentation

- **Architecture**: See [ARCHITECTURE.md](ARCHITECTURE.md) for system design
- **Examples**: See `examples/` directory for usage examples
- **API Reference**: See docstrings in source files

## 🔒 Security Best Practices

- Store API keys in environment variables
- Use OAuth2 for production APIs
- Implement proper error handling
- Log sensitive operations appropriately
- Use HTTPS for all API communications

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

MIT License

## 👤 Author

**Deepa Govinda Panicker**

- GitHub: [@deepapanicker](https://github.com/deepapanicker)
- Portfolio: [deepapanicker.com](https://deepapanicker.com)
