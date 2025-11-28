# Testing Guide - Quick Reference

## 🚀 Quick Start

```bash
# Install test dependencies
make install

# Run all tests
make test

# Run tests with coverage
make test-cov
```

## 📁 Test Structure

```
/Users/gemma.cortel/code/hexagonal/
├── app/                          # Application code
│   ├── domain/                   # ← Tested in tests/unit/domain/
│   ├── application/              # ← Tested in tests/unit/application/
│   ├── infrastructure/           # ← Tested in tests/integration/
│   └── ui/                       # ← Tested in tests/integration/http/
│
└── tests/                        # Test suite
    ├── conftest.py              # Shared pytest fixtures
    ├── pytest.ini               # Pytest configuration
    │
    ├── unit/                    # Fast, isolated tests
    │   ├── domain/
    │   │   └── test_payee.py   # ✅ Domain entity tests
    │   └── application/
    │       └── test_onboard_payee_service.py  # ✅ Service tests
    │
    ├── integration/             # Tests with external systems
    │   ├── database/
    │   │   └── test_payee_repository.py
    │   ├── messaging/
    │   │   └── test_event_publishing.py
    │   ├── http/
    │   │   └── test_payee_api.py  # ✅ API endpoint tests
    │   └── repository/
    │       └── test_repository_integration.py
    │
    ├── component/               # End-to-end component tests
    │   ├── api/
    │   │   └── test_api_component.py
    │   ├── cli/
    │   │   └── test_cli_component.py
    │   └── workers/
    │       └── test_worker_component.py
    │
    └── architecture/            # Architecture compliance
        └── test_hexagonal_rules.py  # ✅ Enforces hexagonal rules
```

## 🧪 Test Commands

| Command | What it does |
|---------|-------------|
| `make test` | Run all tests |
| `make test-cov` | Run tests + generate coverage report |
| `make test-unit` | Run only fast unit tests |
| `make test-integration` | Run integration tests |
| `make test-architecture` | Check architecture compliance |

## ✅ What's Already Tested

### 1. **Unit Tests** (`tests/unit/domain/test_payee.py`)
- ✅ Payee creation
- ✅ Status transitions (activate, mark_as_failed)
- ✅ PSP reference setting

### 2. **Application Tests** (`tests/unit/application/test_onboard_payee_service.py`)
- ✅ Successful onboarding flow
- ✅ Failure handling when PSP fails
- ✅ Repository and event publisher interactions

### 3. **Integration Tests** (`tests/integration/http/test_payee_api.py`)
- ✅ Health check endpoint
- ✅ Onboard payee API endpoint
- ✅ Invalid email validation

### 4. **Architecture Tests** (`tests/architecture/test_hexagonal_rules.py`)
- ✅ Domain has no infrastructure dependencies
- ✅ Domain has no UI dependencies
- ✅ Domain has no framework dependencies
- ✅ Application has no infrastructure dependencies
- ✅ Ports are abstractions (ABC/Protocol)

## 📊 Test Coverage

After running `make test-cov`, view coverage:

**Terminal output**: Shows coverage percentage immediately

**HTML report**: 
```bash
open htmlcov/index.html
```

## 🎯 Test Types Explained

### Unit Tests → Fast & Isolated
```python
# Example: Testing domain logic
def test_create_payee_with_valid_data():
    payee = Payee.create(name="John", email="john@example.com", ...)
    assert payee.status == PayeeStatus.PENDING
```

### Integration Tests → Real Components
```python
# Example: Testing API with TestClient
def test_onboard_payee_endpoint():
    response = client.post("/api/payees", json={...})
    assert response.status_code == 201
```

### Architecture Tests → Compliance
```python
# Example: Enforcing architecture rules
def test_domain_has_no_infrastructure_dependencies():
    # Checks that domain/ doesn't import from infrastructure/
    assert "infrastructure" not in domain_imports
```

## 🔧 Adding New Tests

### 1. Add a Unit Test
```bash
# Create: tests/unit/domain/test_new_feature.py
pytest tests/unit/domain/test_new_feature.py -v
```

### 2. Add an Integration Test
```bash
# Create: tests/integration/database/test_new_repo.py
pytest tests/integration/database/test_new_repo.py -v
```

## 💡 Best Practices

✅ **DO**:
- Write tests before or alongside code (TDD)
- Keep unit tests fast (< 1 second each)
- Mock external dependencies in unit tests
- Use descriptive test names
- Follow the AAA pattern (Arrange, Act, Assert)

❌ **DON'T**:
- Don't make tests depend on each other
- Don't test implementation details
- Don't skip architecture tests
- Don't commit code that breaks tests

## 🐛 Troubleshooting

**Problem**: `ModuleNotFoundError`
```bash
# Solution: Install dependencies
make install
```

**Problem**: Tests not found
```bash
# Solution: Check you're in project root
cd /Users/gemma.cortel/code/hexagonal
pytest tests/
```

**Problem**: Coverage report not generated
```bash
# Solution: Use test-cov target
make test-cov
```

## 📚 Next Steps

1. Run `make test` to verify all tests pass
2. Run `make test-cov` to see current coverage
3. Add tests for new features as you build them
4. Keep architecture tests passing (enforces hexagonal principles)

---

**Full documentation**: See `tests/README.md` for detailed testing guide.

