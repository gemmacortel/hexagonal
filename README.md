# Payee Onboarding Service

A hexagonal architecture application for onboarding payees. This service handles payee creation, PSP (Payment Service Provider) integration, and event publishing.

## Architecture

This project implements **Hexagonal Architecture** (also known as Ports and Adapters), which promotes:

- **Domain-centric design**: Business logic is independent of external frameworks and infrastructure
- **Testability**: Core business logic can be tested in isolation
- **Flexibility**: Easy to swap implementations (e.g., switch databases or PSP providers)

### Project Structure

```
app/
├── domain/              # Core business logic (entities, value objects, domain events)
│   ├── model/          # Domain entities (Payee, PayeeStatus)
│   ├── events/         # Domain events (PayeeOnboardedEvent)
│   ├── exceptions/     # Domain exceptions
│   └── ports/          # Interfaces for external dependencies
├── application/         # Use cases and application services
│   ├── dtos.py         # Data Transfer Objects
│   └── onboard_payee.py  # Onboarding use case
├── infrastructure/      # External adapters (database, PSP, pub/sub)
│   ├── database.py     # Database implementation
│   ├── psp_client.py   # PSP client implementation
│   └── pubsub.py       # Event publishing implementation
└── ui/                 # User interface layer (REST API)
    └── rest/           # FastAPI REST endpoints
```

## Prerequisites

- **Python 3.10+** (recommended 3.11 or higher)
- **pip** (Python package manager)
- Optional: **virtualenv** or **venv** for virtual environment management

## Quick Start (with Makefile)

The easiest way to get started is using the included Makefile:

```bash
# Complete setup (creates venv and installs dependencies)
make setup

# Run the application (venv is used automatically)
make run
```

**No need to manually activate the virtual environment!** The Makefile automatically uses the venv when running commands.

See all available commands:
```bash
make help
```

## Manual Installation

If you prefer not to use the Makefile, you'll need to manually activate the virtual environment:

1. **Clone the repository** (if you haven't already):
   ```bash
   cd /Users/gemma.cortel/code/hexagonal
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment** (required for manual workflow):
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

> **Note**: With manual installation, you must activate the venv in each new terminal session before running commands.

## Running the Application

### Using Makefile (Recommended)

```bash
# Run the application
make run

# Or run in development mode with auto-reload
make dev
```

### Manual Methods

**Method 1: Using Python directly**

```bash
python -m app.main
```

**Method 2: Using Uvicorn**

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The application will start on **http://localhost:8000**

### Verify the Application is Running

Using Makefile:
```bash
make health
```

Or manually with curl:
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "payee-onboarding",
  "version": "1.0.0"
}
```

## Makefile Commands

The project includes a Makefile with convenient shortcuts:

| Command | Description |
|---------|-------------|
| `make help` | Show all available commands |
| `make venv` | Create virtual environment |
| `make install` | Install dependencies |
| `make setup` | Complete setup (venv + install) |
| `make run` | Run the application |
| `make dev` | Run in development mode with auto-reload |
| `make health` | Check if the service is running |
| `make test-api` | Test the API with a sample request |
| `make docs` | Show API documentation URLs |
| `make clean` | Remove cache files and build artifacts |
| `make test` | Run tests (placeholder for future implementation) |
| `make lint` | Run linting (placeholder for future implementation) |
| `make format` | Format code (placeholder for future implementation) |

## API Documentation

Once the application is running, you can access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Health Check

```
GET /health
```

Returns the health status of the service.

### Onboard Payee

```
POST /api/payees
```

Creates a new payee, validates eligibility, onboards them in the PSP, and publishes an event.

**Request Body**:
```json
{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "bank_account": "GB29NWBK60161331926819"
}
```

**Response** (201 Created):
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "John Doe",
  "email": "john.doe@example.com",
  "bank_account": "GB29NWBK60161331926819",
  "status": "ONBOARDED",
  "psp_reference": "PSP-REF-123",
  "created_at": "2025-11-28T10:00:00Z",
  "updated_at": "2025-11-28T10:00:00Z"
}
```

## Development

### Running in Development Mode

The application is configured to run with hot-reload by default, which means changes to the code will automatically restart the server:

```bash
python -m app.main
```

### Project Configuration

- **Host**: `0.0.0.0` (accepts connections from any IP)
- **Port**: `8000`
- **Log Level**: `info`
- **Auto-reload**: Enabled in development

### Adding Production Dependencies

The `requirements.txt` file includes commented-out production dependencies. Uncomment them as needed:

```txt
# For HTTP PSP client integration
httpx==0.26.0

# For GCP Pub/Sub event publishing
google-cloud-pubsub==2.18.4

# For database with SQLAlchemy
sqlalchemy==2.0.25

# For PostgreSQL async driver
asyncpg==0.29.0
```

After uncommenting, reinstall dependencies:
```bash
pip install -r requirements.txt
```

## Testing

### Quick API Test

Using Makefile:
```bash
make test-api
```

### Manual Testing with curl

Create a payee:
```bash
curl -X POST http://localhost:8000/api/payees \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Smith",
    "email": "jane.smith@example.com",
    "bank_account": "GB29NWBK60161331926819"
  }'
```

### Using the Interactive API Docs

1. Navigate to http://localhost:8000/docs
2. Click on the POST /api/payees endpoint
3. Click "Try it out"
4. Enter the request body
5. Click "Execute"

## Architecture Benefits

### Hexagonal Architecture Layers

1. **Domain Layer** (`app/domain/`):
   - Contains business entities and rules
   - Independent of frameworks and external systems
   - Defines ports (interfaces) for external dependencies

2. **Application Layer** (`app/application/`):
   - Orchestrates use cases
   - Coordinates between domain and infrastructure
   - Implements application-specific logic

3. **Infrastructure Layer** (`app/infrastructure/`):
   - Implements ports defined in the domain
   - Handles external integrations (database, PSP, pub/sub)
   - Can be easily swapped or mocked for testing

4. **UI Layer** (`app/ui/`):
   - Exposes the application through REST API
   - Translates HTTP requests to application commands
   - Handles HTTP-specific concerns

### Key Design Patterns

- **Dependency Inversion**: Domain defines interfaces; infrastructure implements them
- **Dependency Injection**: Services receive their dependencies through constructors
- **DTOs**: Clear separation between API contracts and domain models
- **Domain Events**: Decoupled notification of business events

## Quick Reference

### Makefile Workflow (Recommended)

```bash
# First time setup
make setup

# Run the application (venv used automatically)
make run

# Check health
make health

# Test API
make test-api

# View documentation
make docs

# Clean up
make clean
```

> **Note**: When using the Makefile, you don't need to manually activate the virtual environment. It's automatically detected and used.

### Manual Workflow

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python -m app.main

# Verify it's running
curl http://localhost:8000/health
```

## Troubleshooting

### Port Already in Use

If port 8000 is already in use, you can change it:

```bash
uvicorn app.main:app --reload --port 8001
```

### Import Errors

Make sure you're running the application from the project root and that your virtual environment is activated.

### Module Not Found

Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

## License

[Your License Here]

## Contributing

[Your Contributing Guidelines Here]

## Contact

[Your Contact Information Here]

