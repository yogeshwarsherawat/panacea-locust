# Panacea API Load Testing Framework

A comprehensive, independent Locust-based load testing framework for the Panacea API insights endpoints. This framework provides realistic user simulation with user-specific payload generation, session management, and formal data distribution.

## 🏗️ Architecture

### Project Structure
```
panacea-locust/
├── locustfile.py          # Main orchestrator (simple imports)
├── base_user.py          # Base PanaceaAPIUser class with core functionality
├── user_types.py         # Simplified user classes (Heavy, Light only)
├── tasks/                # Task groups organized by API functionality
│   ├── __init__.py       # Combined StandardTaskMixin
│   ├── logs_tasks.py     # Logs API endpoints
│   ├── events_tasks.py   # Events API endpoints
│   ├── ai_tasks.py       # AI API endpoints
│   └── reports_tasks.py  # Reports API endpoints
├── event_handlers.py     # Event monitoring and test lifecycle management
├── payload_generator.py  # User-specific payload generation and data pools
├── config.py            # Centralized configuration management
├── requirements.txt     # Python dependencies
├── results/             # Test results and summaries (auto-created)
└── README.md           # This documentation
```

### Simplified Design Benefits
- **Easy Setup**: Just Heavy and Light users - perfect for quick testing
- **Organized Tasks**: API endpoints grouped by functionality in tasks/ folder
- **One-Day Ready**: Streamlined for rapid deployment and testing
- **Clear Structure**: Easy to understand and modify
- **Focused Testing**: Covers all endpoints with simple user patterns

### Key Features
- **Independent Framework**: Completely separate from panacea-api
- **User-Specific Data**: Each virtual user has unique bundle IDs, session IDs, and data pools
- **Session Management**: X-Session-Id headers for all requests
- **Formal Distribution**: Controlled overlap and realistic data spread
- **Modular Design**: Easy to extend and modify for future requirements
- **Database Ready**: Designed for easy migration from random to database-driven payloads

### Module Overview

#### 🎭 **user_types.py** - Simplified User Classes
- **HeavyUser**: High-frequency requests (Weight: 1, Wait: 0.5-1s)
- **LightUser**: Low-frequency requests (Weight: 3, Wait: 2-4s)

#### 🎯 **tasks/** - Organized Task Groups
- **logs_tasks.py**: All logs-related endpoints (analyze, info, search, etc.)
- **events_tasks.py**: Events API tasks
- **ai_tasks.py**: AI and ML endpoints
- **reports_tasks.py**: Reports and admin tasks
- **__init__.py**: Combined StandardTaskMixin for all users

#### 🏗️ **base_user.py** - Core Functionality
- Session management and headers
- HTTP request handling with error management
- User initialization and data pool registration
- Common utilities and logging

#### 📊 **event_handlers.py** - Monitoring & Metrics
- Test lifecycle management (start/stop events)
- User registration tracking
- Performance monitoring
- Test summary generation and export
- Real-time logging and debugging

#### 🎲 **payload_generator.py** - Data Generation
- User-specific data pools and ranges
- Realistic payload generation for all endpoints
- Bundle ID and Combo ID distribution
- Session ID management
- Future database integration support

#### ⚙️ **config.py** - Configuration Management
- Environment variable support
- User distribution weights
- API endpoint configuration
- Data generation parameters
- Validation and defaults

## 🚀 Quick Start

### Installation
```bash
# Clone or navigate to the panacea-locust directory
cd panacea-locust

# Install dependencies
pip install -r requirements.txt

# Set up ClickHouse environment (choose one method)
# Method 1: Use setup script (recommended)
source setup_env.sh

# Method 2: Use Python setup and test script
python setup_and_test.py

# Method 3: Manual environment variables
export CLICKHOUSE_HOST="panacea-clickhouse.cpaasonprem.com"
export CLICKHOUSE_PORT="9000"
export CLICKHOUSE_DATABASE="panacea"
export CLICKHOUSE_USER="panacea_user"
export CLICKHOUSE_PASSWORD="qwerty"
export USE_DATABASE_DATA="true"

# Run basic load test
locust -f locustfile.py --host=https://your-api-server.com
```

### Basic Usage
```bash
# Interactive mode with web UI
locust -f locustfile.py --host=https://your-api-server.com

# Headless mode with specific parameters
locust -f locustfile.py --host=https://your-api-server.com -u 50 -r 5 -t 300s --headless

# With results export
locust -f locustfile.py --host=https://your-api-server.com -u 30 -r 4 -t 600s --headless --csv=results --html=report.html
```

## 🎯 User Types and Distribution

### Simplified User Classes
1. **HeavyUser** (Weight: 1)
   - Wait time: 0.5-1 seconds
   - High-frequency requests for stress testing
   - Uses all API endpoints with standard weights
   
2. **LightUser** (Weight: 3)
   - Wait time: 2-4 seconds
   - Low-frequency requests for normal usage patterns
   - Uses all API endpoints with standard weights

### Data Distribution
- **Bundle IDs**: Each user gets a range of 50 bundle IDs with 30% overlap
- **Combo IDs**: Each user gets a range of 20 combo IDs
- **Session IDs**: Unique 32-character hex session ID per user
- **SFDC Cases**: Pool of 10 case numbers per user around a base case

## 🔧 Configuration

### Environment Variables
All configuration can be customized via environment variables:

```bash
# API Configuration
export PANACEA_HOST=https://your-api-server.com
export LOCUST_MIN_USERS=1
export LOCUST_MAX_USERS=100
export LOCUST_SPAWN_RATE=2

# Bundle ID Configuration
export BUNDLE_ID_MIN=800
export BUNDLE_ID_MAX=1000
export BUNDLE_ID_RANGE_PER_USER=50
export BUNDLE_ID_OVERLAP_PERCENTAGE=0.3

# User Configuration
export USER_POOL_SIZE=1000
export USER_ID_PREFIX=loadtest_user

# Wait Time Configuration
export STANDARD_WAIT_MIN=1.0
export STANDARD_WAIT_MAX=2.0
export HEAVY_WAIT_MIN=0.5
export HEAVY_WAIT_MAX=1.0
```

### ClickHouse Database Configuration

The framework supports both random data generation and real database data:

#### Environment Variables for ClickHouse
```bash
# ClickHouse Connection
export CLICKHOUSE_HOST="panacea-clickhouse.cpaasonprem.com"
export CLICKHOUSE_PORT="9000"
export CLICKHOUSE_DATABASE="panacea"
export CLICKHOUSE_USER="panacea_user"
export CLICKHOUSE_PASSWORD="qwerty"

# Database Integration Control
export USE_DATABASE_DATA="true"        # Enable/disable database data loading
export DB_USERS_LIMIT="1000"          # Max users to fetch from DB
export DB_BUNDLE_IDS_LIMIT="500"      # Max bundle IDs to fetch from DB
export DB_COMBO_IDS_LIMIT="100"       # Max combo IDs to fetch from DB
export DB_SFDC_CASES_LIMIT="200"      # Max SFDC cases to fetch from DB
```

#### Testing ClickHouse Connection
```bash
# Test connection and view database info
python setup_and_test.py

# Test with detailed ClickHouse queries
python test_clickhouse.py
```

#### Database vs Random Data
- **Database Mode** (`USE_DATABASE_DATA=true`): Loads real user sessions, bundle IDs, combo IDs, and SFDC cases from ClickHouse
- **Random Mode** (`USE_DATABASE_DATA=false`): Generates realistic random data for testing
- **Fallback**: Automatically falls back to random data if database connection fails

### Configuration File
Edit `config.py` to modify default settings:
- Bundle ID ranges and distribution
- User weights and wait times
- API endpoints and timeouts
- Data generation templates
- ClickHouse connection parameters

## 📊 API Endpoints Tested

### Logs Endpoints
- `POST /api/v1/logs/analyze` - Analyze log bundles (Weight: 3)
- `GET /api/v1/logs/info` - Get logs information (Weight: 4)
- `POST /api/v1/logs/severity-count` - Get severity counts (Weight: 3)
- `POST /api/v1/logs/histogram` - Get histogram data (Weight: 2)
- `POST /api/v1/logs/heatmap` - Get heatmap data (Weight: 2)
- `POST /api/v1/logs/search` - Search logs (Weight: 3)
- `GET /api/v1/logs/filter-options` - Get filter options (Weight: 2)

### Events Endpoints
- `GET /api/v1/events` - Get events by bundle or combo ID (Weight: 2)

### AI Endpoints
- `GET /api/v1/ai/report_summary` - Get AI report summary (Weight: 1)
- `POST /api/v1/ai/ask-ai` - Ask AI questions (Weight: 1)

### Reports Endpoints
- `POST /api/v1/reports` - Get reports with filtering (Weight: 2)
- `GET /api/v1/log-bundle-paths/by-sfdc-case/{id}` - Get bundle paths (Weight: 1)

## 🎲 Payload Generation

### User-Specific Data Pools
Each user maintains pools of:
- **Bundle IDs**: 50 unique IDs within user's range
- **Combo IDs**: 20 unique IDs within user's range
- **SFDC Cases**: 10 case numbers around user's base case
- **Log Bundle Paths**: 15 realistic file paths
- **Session ID**: Unique session identifier

### Realistic Data Generation
- **Log Messages**: Template-based with realistic variables
- **Timestamps**: ISO format with proper time ranges
- **IP Addresses**: Private IP ranges (10.x.x.x, 172.16-31.x.x, 192.168.x.x)
- **Components**: Real Nutanix component names
- **UUIDs**: Properly formatted UUIDs

### Sample Payloads

#### Logs Analyze Request
```json
{
  "remote_log_bundle_path": "/users/john.doe/NTNX-Log-2024-01-15-12345-1705123456-PE-10.1.1.100.zip",
  "sfdc_case_no": "012345678",
  "is_retry": false
}
```

#### Logs Search Request
```json
{
  "bundle_ids": [838, 839],
  "page_size": 20,
  "page_no": 1,
  "filters": {
    "components": ["acropolis", "stargate"],
    "log_levels": ["error", "warn"],
    "cvm_ips": ["10.1.1.100"],
    "start_time": "2024-01-15T10:00:00Z",
    "end_time": "2024-01-15T12:00:00Z",
    "search_log_string": "Cassandra",
    "is_curated": false
  }
}
```

## 🔍 Session Management

### X-Session-Id Header
Every request includes a unique session ID:
```http
X-Session-Id: a1b2c3d4e5f6789012345678901234567890abcd
Authorization: Bearer mock-token-loadtest_user_1234567890_12345
Content-Type: application/json
User-Agent: PanaceaLocust/1.0 User-loadtest_user_1234567890_12345
```

### Session Lifecycle
- Generated on user startup
- Maintained throughout user's lifecycle
- Unique per virtual user instance
- 32-character hexadecimal format

## 📈 Monitoring and Results

### Web Interface
Access the Locust web UI at `http://localhost:8089` to:
- Monitor real-time statistics
- View response times and failure rates
- Control test execution
- Download results

### Key Metrics
- **Requests per Second**: Overall throughput
- **Response Times**: 50th, 95th, 99th percentiles
- **Failure Rate**: Percentage of failed requests
- **User Distribution**: Active users by type

### Expected Response Codes
- `200`: Success
- `400`: Bad Request (acceptable for test data)
- `404`: Not Found (acceptable for non-existent resources)
- `500`: Server Error (investigate if frequent)

## 🔄 ClickHouse Database Integration

The framework now supports both random and database-driven payloads:

### Database-Driven Mode (Current Implementation)
```python
# payload_generator.py - with ClickHouse integration
def _initialize_database_data(self):
    """Initialize database data pools if enabled."""
    if config.USE_DATABASE_DATA:
        try:
            if clickhouse_dao.test_connection():
                self.db_users_sessions = clickhouse_dao.get_users_and_sessions(
                    limit=config.DB_USERS_LIMIT
                )
                self.db_bundle_ids = clickhouse_dao.get_active_bundle_ids(
                    limit=config.DB_BUNDLE_IDS_LIMIT
                )
                # ... load other data types
        except Exception as e:
            logger.error(f"Failed to initialize database data: {str(e)}")
            # Falls back to random generation
```

### Hybrid Approach (Smart Fallback)
```python
# payload_generator.py
def generate_logs_analyze_payload(self, user_id: str):
    user_pool = self.get_user_pool(user_id)
    return {
        "remote_log_bundle_path": user_pool.get_log_bundle_path(),
        "sfdc_case_no": user_pool.get_sfdc_case(),  # Uses DB data if available
        "is_retry": random.choice([True, False])
    }
```

### ClickHouse Data Sources
- **User Sessions**: Real user IDs and session IDs from `user_sessions` table
- **Bundle IDs**: Active bundle IDs from production data
- **Combo IDs**: Active combo bundle IDs from production data  
- **SFDC Cases**: Recent SFDC case numbers from production data

## 🛠️ Development and Customization

### Adding New Endpoints
1. Add endpoint configuration to `config.py`
2. Create payload generation method in `payload_generator.py`
3. Add task method to appropriate user class in `locustfile.py`

### Modifying Data Distribution
1. Update range configurations in `config.py`
2. Modify distribution logic in `payload_generator.py`
3. Test with small user counts first

### Custom User Types
```python
class CustomUser(PanaceaAPIUser):
    weight = 2
    
    @task(10)
    def custom_task(self):
        # Custom task implementation
        payload = payload_generator.generate_custom_payload(self.user_id)
        self._make_request("POST", "custom/endpoint", json_data=payload)
```

## 🚨 Troubleshooting

### Common Issues
1. **Import Errors**: Ensure all dependencies are installed via `requirements.txt`
2. **Configuration Errors**: Check environment variables and `config.py` validation
3. **Connection Errors**: Verify host URL and network connectivity
4. **High Failure Rates**: Check API server capacity and payload validity

### Debug Mode
Enable detailed logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Performance Tips
1. Start with low user counts (5-10 users)
2. Monitor server resources during testing
3. Use realistic test duration (10-30 minutes)
4. Test during off-peak hours

## 📋 Test Scenarios

### Smoke Test
```bash
locust -f locustfile.py --host=https://your-api-server.com -u 5 -r 1 -t 60s --headless
```

### Load Test
```bash
locust -f locustfile.py --host=https://your-api-server.com -u 25 -r 3 -t 600s --headless
```

### Stress Test
```bash
locust -f locustfile.py --host=https://your-api-server.com -u 100 -r 10 -t 1800s --headless
```

### Analytics Focus Test
```bash
# Set higher weight for analytics users
export ANALYTICS_USER_WEIGHT=5
locust -f locustfile.py --host=https://your-api-server.com -u 50 -r 5 -t 900s --headless
```

## 🤝 Contributing

1. Follow the existing code structure and patterns
2. Update configuration in `config.py` for new features
3. Add comprehensive docstrings and comments
4. Test with small user counts before large-scale testing
5. Update this README for significant changes

## 📄 License

This load testing framework is part of the Panacea project and follows the same licensing terms.
