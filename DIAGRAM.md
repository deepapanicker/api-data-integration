# API Data Integration - Visual Architecture Diagram

## System Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    API Data Integration Framework                        │
│                         Complete ETL Pipeline                             │
└─────────────────────────────────────────────────────────────────────────┘
```

## Component Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│                           Configuration Layer                             │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │                    api_config.yaml                                  │  │
│  │  • API endpoints                                                   │  │
│  │  • Authentication settings                                         │  │
│  │  • Rate limiting rules                                             │  │
│  │  • Retry policies                                                  │  │
│  └────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                          API Clients Layer                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                 │
│  │ BaseClient   │  │ RESTClient    │  │ OAuthClient  │                 │
│  │ (Abstract)   │  │              │  │              │                 │
│  │              │  │ • API Key    │  │ • OAuth2     │                 │
│  │ • Retry      │  │ • Headers    │  │ • Token mgmt │                 │
│  │ • Timeout    │  │ • JSON        │  │ • Auto-refresh│                │
│  │ • Session    │  │              │  │              │                 │
│  └──────────────┘  └──────────────┘  └──────────────┘                 │
└──────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                         Extraction Layer                                  │
│  ┌──────────────────────┐  ┌──────────────────────────┐                  │
│  │   APIExtractor      │  │ IncrementalExtractor     │                  │
│  │                     │  │                          │                  │
│  │ • Full extraction   │  │ • Incremental sync      │                  │
│  │ • Pagination        │  │ • Timestamp filtering    │                  │
│  │ • Batch processing  │  │ • Last sync tracking     │                  │
│  │ • Multiple formats  │  │ • Change detection       │                  │
│  └──────────────────────┘  └──────────────────────────┘                  │
└──────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                      Transformation Layer                                 │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │              ResponseTransformer                                    │  │
│  │                                                                    │  │
│  │  • Field mapping (API → Target)                                   │  │
│  │  • Data normalization                                              │  │
│  │  • Nested structure flattening                                     │  │
│  │  • Date/time formatting                                            │  │
│  │  • Custom transformation functions                                 │  │
│  └────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                          Loading Layer                                    │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │                    DatabaseLoader                                   │  │
│  │                                                                    │  │
│  │  • Append mode (insert new records)                                │  │
│  │  • Replace mode (truncate and reload)                              │  │
│  │  • Upsert mode (insert or update)                                  │  │
│  │  • Batch loading (chunked inserts)                                  │  │
│  │  • Transaction support                                             │  │
│  └────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                        Utility Services                                   │
│  ┌──────────────────────┐  ┌──────────────────────┐                     │
│  │   RateLimiter       │  │   ErrorHandler       │                     │
│  │                     │  │                      │                     │
│  │ • Per-second limit  │  │ • Error logging      │                     │
│  │ • Per-minute limit  │  │ • Error tracking     │                     │
│  │ • Sliding window    │  │ • Retry logic        │                     │
│  │ • Auto-throttling   │  │ • Error history      │                     │
│  └──────────────────────┘  └──────────────────────┘                     │
└──────────────────────────────────────────────────────────────────────────┘
```

## Data Flow Diagram

```
┌─────────────┐
│   API       │
│   Source    │
│             │
│  REST API   │
│  OAuth API  │
└──────┬──────┘
       │
       │ HTTP Request
       │ (GET/POST/PUT/DELETE)
       ▼
┌─────────────────────────────────────┐
│         API Client                  │
│  ┌───────────────────────────────┐  │
│  │ 1. Authentication             │  │
│  │    • API Key / OAuth Token    │  │
│  │ 2. Rate Limiting              │  │
│  │    • Wait if needed           │  │
│  │ 3. Request Execution          │  │
│  │    • Retry on failure         │  │
│  │ 4. Response Handling          │  │
│  │    • Parse JSON/XML           │  │
│  └───────────────────────────────┘  │
└──────────────┬──────────────────────┘
               │
               │ Raw API Response
               │ (JSON/XML)
               ▼
┌─────────────────────────────────────┐
│      API Extractor                  │
│  ┌───────────────────────────────┐  │
│  │ 1. Pagination Handling        │  │
│  │    • Fetch all pages          │  │
│  │ 2. Data Parsing               │  │
│  │    • Extract records          │  │
│  │ 3. Incremental Logic          │  │
│  │    • Filter by timestamp      │  │
│  │ 4. Batch Collection           │  │
│  │    • Aggregate results        │  │
│  └───────────────────────────────┘  │
└──────────────┬──────────────────────┘
               │
               │ List of Records
               │ (List[Dict])
               ▼
┌─────────────────────────────────────┐
│   Response Transformer              │
│  ┌───────────────────────────────┐  │
│  │ 1. Field Mapping             │  │
│  │    • Rename fields           │  │
│  │ 2. Data Normalization        │  │
│  │    • Format dates            │  │
│  │    • Clean strings            │  │
│  │ 3. Structure Flattening       │  │
│  │    • Unnest nested objects   │  │
│  │ 4. Custom Transforms         │  │
│  │    • Apply business rules     │  │
│  └───────────────────────────────┘  │
└──────────────┬──────────────────────┘
               │
               │ Transformed Records
               │ (Normalized List[Dict])
               ▼
┌─────────────────────────────────────┐
│    Database Loader                  │
│  ┌───────────────────────────────┐  │
│  │ 1. Connection Management     │  │
│  │    • Create DB connection    │  │
│  │ 2. Load Strategy              │  │
│  │    • Append/Replace/Upsert   │  │
│  │ 3. Batch Processing          │  │
│  │    • Chunked inserts         │  │
│  │ 4. Transaction Control       │  │
│  │    • Commit/rollback         │  │
│  └───────────────────────────────┘  │
└──────────────┬──────────────────────┘
               │
               │ SQL INSERT/UPDATE
               ▼
┌─────────────┐
│  Database   │
│  (Target)   │
│             │
│ PostgreSQL  │
│ MySQL       │
│ SQL Server  │
└─────────────┘
```

## Incremental Sync Flow

```
┌─────────────────────────────────────────────────────────────┐
│              Incremental Sync Process                       │
└─────────────────────────────────────────────────────────────┘

┌──────────────┐
│  First Run   │
└──────┬───────┘
       │
       │ No last_sync.json
       ▼
┌─────────────────────────────┐
│ Extract ALL Records         │
│ • No timestamp filter       │
│ • Get all data              │
└──────┬──────────────────────┘
       │
       │ Save latest timestamp
       ▼
┌─────────────────────────────┐
│ Create last_sync.json       │
│ {                           │
│   "last_sync": "2024-01-01" │
│ }                           │
└─────────────────────────────┘

┌──────────────┐
│ Next Run     │
└──────┬───────┘
       │
       │ Load last_sync.json
       ▼
┌─────────────────────────────┐
│ Extract NEW Records         │
│ • Filter: updated_at >     │
│   last_sync                │
│ • Only changed data         │
└──────┬──────────────────────┘
       │
       │ Update timestamp
       ▼
┌─────────────────────────────┐
│ Update last_sync.json      │
│ {                           │
│   "last_sync": "2024-01-02" │
│ }                           │
└─────────────────────────────┘
```

## OAuth2 Authentication Flow

```
┌─────────────────────────────────────────────────────────────┐
│              OAuth2 Authentication Flow                     │
└─────────────────────────────────────────────────────────────┘

┌──────────────┐
│ Initialize   │
│ OAuthClient  │
└──────┬───────┘
       │
       │ client_id, client_secret, token_url
       ▼
┌─────────────────────────────┐
│ Request Access Token        │
│ POST /oauth/token           │
│ {                           │
│   "grant_type": "client_    │
│    credentials",            │
│   "client_id": "...",       │
│   "client_secret": "..."    │
│ }                           │
└──────┬──────────────────────┘
       │
       │ Response: access_token, expires_in
       ▼
┌─────────────────────────────┐
│ Store Token                 │
│ • access_token              │
│ • expires_at = now +        │
│   expires_in                │
└──────┬──────────────────────┘
       │
       │ Use token for API requests
       ▼
┌─────────────────────────────┐
│ Make API Request            │
│ GET /api/data               │
│ Header:                     │
│   Authorization: Bearer      │
│   {access_token}            │
└──────┬──────────────────────┘
       │
       │ Check expiration before each request
       ▼
┌─────────────────────────────┐
│ Token Expired?              │
│ • Check expires_at          │
│ • If expired, re-authenticate│
└──────┬──────────────────────┘
       │
       │ Auto-refresh
       ▼
┌─────────────────────────────┐
│ Re-authenticate            │
│ (Repeat token request)      │
└─────────────────────────────┘
```

## Rate Limiting Strategy

```
┌─────────────────────────────────────────────────────────────┐
│              Rate Limiting Implementation                   │
└─────────────────────────────────────────────────────────────┘

Per-Second Limit:
┌─────────────────────────────────────┐
│ Calculate:                          │
│ min_interval = 1 / req_per_sec      │
│                                     │
│ Before each request:                │
│ • time_since_last = now - last_req  │
│ • if time_since_last < min_interval:│
│   → sleep(min_interval -            │
│        time_since_last)             │
└─────────────────────────────────────┘

Per-Minute Limit:
┌─────────────────────────────────────┐
│ Maintain sliding window:            │
│ • Track request timestamps          │
│ • Remove requests > 60s old        │
│                                     │
│ Before each request:                │
│ • count = len(recent_requests)      │
│ • if count >= limit:                │
│   → wait until oldest expires       │
└─────────────────────────────────────┘
```

## Error Handling Flow

```
┌─────────────────────────────────────────────────────────────┐
│              Error Handling Process                         │
└─────────────────────────────────────────────────────────────┘

┌──────────────┐
│ API Request  │
└──────┬───────┘
       │
       │ Error occurs
       ▼
┌─────────────────────────────┐
│ ErrorHandler.handle_error() │
│ • Capture exception         │
│ • Extract error details     │
│ • Get context info          │
└──────┬──────────────────────┘
       │
       │ Log error
       ▼
┌─────────────────────────────┐
│ Log to File                 │
│ • Timestamp                 │
│ • Error type                │
│ • Error message             │
│ • Stack trace               │
│ • Context                   │
└──────┬──────────────────────┘
       │
       │ Add to history
       ▼
┌─────────────────────────────┐
│ Error History               │
│ • Track all errors          │
│ • Generate summary          │
│ • Error statistics          │
└─────────────────────────────┘
```

## Complete ETL Pipeline Example

```
┌─────────────────────────────────────────────────────────────┐
│              Complete ETL Pipeline                         │
└─────────────────────────────────────────────────────────────┘

1. Initialize
   └─> RESTClient(base_url, api_key)
       └─> APIExtractor(client)
           └─> ResponseTransformer()
               └─> DatabaseLoader(conn_string)

2. Extract
   └─> extractor.extract('/customers', pagination=True)
       └─> Returns: [{"id": 1, "name": "..."}, ...]

3. Transform
   └─> transformer.transform(data, field_mapping)
       └─> Returns: [{"customer_id": 1, "customer_name": "..."}, ...]

4. Load
   └─> loader.load(data, table='customers', mode='upsert')
       └─> Returns: {"records_loaded": 100, "status": "success"}

5. Monitor
   └─> error_handler.get_error_summary()
       └─> Returns: {"total_errors": 0, "status": "healthy"}
```

