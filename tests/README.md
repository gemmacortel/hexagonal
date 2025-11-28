# Test Suite

This directory contains the comprehensive test suite for the Payee Onboarding Service, following hexagonal architecture principles.

## Test Structure

```
tests/
├── conftest.py              # Shared pytest fixtures and configuration
├── unit/                    # Unit tests (fast, isolated, no external dependencies)
│   ├── domain/             # Domain entity and value object tests
│   └── application/        # Application service tests (with mocked ports)
├── integration/             # Integration tests (test with real external services)
│   ├── database/           # Database integration tests
│   ├── messaging/          # Event publishing integration tests
│   ├── http/               # HTTP API integration tests
│   └── repository/         # Repository implementation tests
├── component/               # Component tests (end-to-end within a component)
    ├── api/                # API component tests
    ├── cli/                # CLI component tests
    └── workers/            # Background worker tests

```

## Test Types

### Unit Tests (`tests/unit/`)

**Purpose**: Test individual units in isolation
- **Speed**: Very fast (< 1 second per test)
- **Dependencies**: All external dependencies are mocked
- **Scope**: Single class or function

**Examples**:
- Domain entity behavior
- Value object validation
- Application service orchestration (with mocked repositories/clients)

**Run**: `make test-unit`

### Integration Tests (`tests/integration/`)

**Purpose**: Test integration with external systems
- **Speed**: Slower (may take seconds)
- **Dependencies**: Real or test doubles of external systems
- **Scope**: Multiple components working together

**Examples**:
- Database operations
- Message queue publishing
- HTTP API endpoints with real services
- Repository implementations

**Run**: `make test-integration`

### Component Tests (`tests/component/`)

**Purpose**: Test complete features end-to-end within a component
- **Speed**: Medium to slow
- **Dependencies**: Real implementations where possible
- **Scope**: Complete user flows

**Examples**:
- Full API workflows
- CLI command execution
- Background job processing

## Running Tests

### All Tests
```bash
make test
```

### With Coverage
```bash
make test-cov
```

View HTML coverage report:
```bash
open htmlcov/index.html
```

### Specific Test Types
```bash
make test-unit              # Fast unit tests only
make test-integration       # Integration tests only
make test-architecture      # Architecture compliance tests
```

### Specific Test File
```bash
pytest tests/unit/domain/test_payee.py -v
```

### Specific Test Function
```bash
pytest tests/unit/domain/test_payee.py::TestPayeeCreation::test_create_payee_with_valid_data -v
```

## Writing Tests

### Unit Test Example

```python
from unittest.mock import Mock
import pytest
from app.application.onboard_payee import OnboardPayeeService

def test_onboard_payee_success():
    # Arrange
    mock_repository = Mock()
    mock_psp_client = Mock()
    mock_event_publisher = Mock()
    
    service = OnboardPayeeService(
        repository=mock_repository,
        psp_client=mock_psp_client,
        publish_payee_onboarded_event=mock_event_publisher
    )
    
    # Act
    result = service.execute(request)
    
    # Assert
    assert mock_repository.save.called
    assert result.status == "ONBOARDED"
```

### Integration Test Example

```python
from fastapi.testclient import TestClient
from app.main import create_app

def test_onboard_payee_endpoint():
    # Arrange
    client = TestClient(create_app())
    
    # Act
    response = client.post("/api/payees", json={
        "name": "John Doe",
        "email": "john@example.com",
        "bank_account": "GB29NWBK60161331926819"
    })
    
    # Assert
    assert response.status_code == 201
    assert response.json()["status"] == "ONBOARDED"
```

## Test Markers

Use pytest markers to categorize tests:

```python
@pytest.mark.unit
def test_fast_unit():
    pass

@pytest.mark.integration
def test_with_database():
    pass

@pytest.mark.slow
def test_long_running():
    pass
```

Run marked tests:
```bash
pytest -m unit        # Run only unit tests
pytest -m integration # Run only integration tests
pytest -m "not slow"  # Skip slow tests
```

## Fixtures

Common fixtures are defined in `conftest.py`:

```python
@pytest.fixture
def sample_payee_data():
    """Sample payee data for testing."""
    return {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "bank_account": "GB29NWBK60161331926819"
    }
```

## Best Practices

### 1. Follow AAA Pattern
- **Arrange**: Set up test data and dependencies
- **Act**: Execute the code under test
- **Assert**: Verify the results

### 2. Test Naming
- Use descriptive names: `test_<what>_<condition>_<expected_result>`
- Example: `test_create_payee_with_invalid_email_raises_validation_error`

### 3. One Assertion per Test (when possible)
- Each test should verify one specific behavior
- Use multiple tests for multiple scenarios

### 4. Use Mocks for External Dependencies
- Mock databases, APIs, message queues in unit tests
- Use real implementations in integration tests

### 5. Keep Tests Fast
- Unit tests should run in milliseconds
- Use test doubles to avoid slow I/O operations

### 6. Test Edge Cases
- Valid inputs
- Invalid inputs
- Boundary conditions
- Error conditions

### 7. Maintain Test Independence
- Tests should not depend on each other
- Each test should clean up after itself
- Use fixtures for common setup

## Coverage Goals

- **Overall**: > 80%
- **Domain Layer**: > 90%
- **Application Layer**: > 85%
- **Infrastructure**: > 70%

## Continuous Integration

Tests should be run:
- Before every commit (pre-commit hook)
- On every pull request
- Before deployment

## Troubleshooting

### Import Errors
Make sure you're in the project root and the virtual environment is activated:
```bash
cd /Users/gemma.cortel/code/hexagonal
source venv/bin/activate
pytest
```

### Module Not Found
Install test dependencies:
```bash
make install
```

### Tests Not Discovered
Check pytest configuration in `pytest.ini` and ensure test files follow naming conventions:
- Files: `test_*.py` or `*_test.py`
- Classes: `Test*`
- Functions: `test_*`

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Hexagonal Architecture Testing](https://herbertograca.com/2017/11/16/explicit-architecture-01-ddd-hexagonal-onion-clean-cqrs-how-i-put-it-all-together/)
- [Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html)

