# API Data Integration - Architecture Diagram

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    API Data Integration Framework                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────┐
│  Configuration  │
│  (api_config.yaml)│
└────────┬─────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│                         API Clients Layer                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐     │
│  │ BaseClient   │    │ RESTClient   │    │ OAuthClient  │     │
│  │ (Abstract)   │◄───┤ (API Key)    │    │ (OAuth2)     │     │
│  └──────────────┘    └──────────────┘    └──────────────┘     │
│                                                                 │
│  • Authentication                                               │
│  • Request/Response handling                                    │
│  • Retry logic                                                  │
│  • Error handling                                               │
└─────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Extraction Layer                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────┐    ┌──────────────────────┐               │
│  │  APIExtractor   │    │ IncrementalExtractor│               │
│  │                 │    │                     │               │
│  │ • Full extract  │    │ • Incremental sync  │               │
│  │ • Pagination    │    │ • Timestamp-based   │               │
│  │ • Batch process │    │ • Last sync tracking│               │
│  └──────────────────┘    └──────────────────────┘               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Transformation Layer                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────┐                                      │
│  │ ResponseTransformer  │                                      │
│  │                      │                                      │
│  │ • Field mapping      │                                      │
│  │ • Data normalization│                                      │
│  │ • Nested flattening  │                                      │
│  │ • Custom transforms  │                                      │
│  └──────────────────────┘                                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Loading Layer                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────┐                                      │
│  │  DatabaseLoader      │                                      │
│  │                      │                                      │
│  │ • Append mode        │                                      │
│  │ • Replace mode       │                                      │
│  │ • Upsert mode        │                                      │
│  │ • Batch loading      │                                      │
│  └──────────────────────┘                                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                        Utility Layer                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐         ┌──────────────┐                     │
│  │ RateLimiter  │         │ErrorHandler  │                     │
│  │              │         │              │                     │
│  │ • Per second │         │ • Logging    │                     │
│  │ • Per minute │         │ • Tracking   │                     │
│  └──────────────┘         └──────────────┘                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

```
┌──────────┐
│   API    │
│  Source  │
└────┬─────┘
     │
     │ HTTP Request
     ▼
┌──────────────┐
│ API Client   │──┐
│ (Auth/Retry) │  │
└──────┬───────┘  │
       │          │ Rate Limiting
       │          │
       ▼          │
┌──────────────┐  │
│  Extractor   │◄─┘
│  (Get Data)  │
└──────┬───────┘
       │
       │ Raw Data
       ▼
┌──────────────┐
│ Transformer  │
│ (Normalize)  │
└──────┬───────┘
       │
       │ Transformed Data
       ▼
┌──────────────┐
│   Loader     │
│  (Database)  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Database   │
│   (Target)   │
└──────────────┘
```

## Component Interaction

```
┌─────────────────────────────────────────────────────────────┐
│                    Example: Full Pipeline                    │
└─────────────────────────────────────────────────────────────┘

1. Initialize Client
   └─> RESTClient(base_url, api_key)
       └─> Handles authentication, retries

2. Extract Data
   └─> APIExtractor(client)
       └─> extract(endpoint, pagination=True)
           └─> Returns: List[Dict]

3. Transform Data
   └─> ResponseTransformer()
       └─> transform(data, field_mapping)
           └─> Returns: List[Dict] (normalized)

4. Load Data
   └─> DatabaseLoader(connection_string)
       └─> load(data, table_name, mode='upsert')
           └─> Returns: Load result

5. Error Handling (throughout)
   └─> ErrorHandler()
       └─> Logs errors, tracks history
```

## Incremental Sync Flow

```
┌─────────────────────────────────────────────────────────────┐
│              Incremental Sync Process                        │
└─────────────────────────────────────────────────────────────┘

First Run:
  └─> No last_sync.json
      └─> Extract ALL records
          └─> Save latest timestamp → last_sync.json

Subsequent Runs:
  └─> Load last_sync.json
      └─> Extract records WHERE updated_at > last_sync
          └─> Update last_sync.json with new latest timestamp
              └─> Only process new/changed records
```

## Authentication Flow (OAuth2)

```
┌─────────────────────────────────────────────────────────────┐
│                    OAuth2 Flow                                │
└─────────────────────────────────────────────────────────────┘

1. Initialize OAuthClient
   └─> client_id, client_secret, token_url

2. Authenticate
   └─> POST token_url
       └─> Receive access_token + expires_in

3. Store Token
   └─> Use token for API requests
       └─> Check expiration before each request

4. Auto-Refresh
   └─> If expired, re-authenticate automatically
```

## Rate Limiting Strategy

```
┌─────────────────────────────────────────────────────────────┐
│              Rate Limiting Implementation                    │
└─────────────────────────────────────────────────────────────┘

Per-Second Limit:
  └─> Calculate min_interval = 1 / requests_per_second
      └─> Sleep if time_since_last < min_interval

Per-Minute Limit:
  └─> Track request timestamps
      └─> If count >= limit, wait until oldest expires
          └─> Maintain sliding window
```

