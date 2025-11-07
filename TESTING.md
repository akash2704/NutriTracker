# Testing Documentation

## Overview

This project includes comprehensive testing for both backend and frontend components, with support for both SQLite (testing) and PostgreSQL (production) databases.

## Backend Testing

### Test Structure
```
backend/tests/
├── conftest.py              # Test configuration and fixtures
├── test_auth.py            # Authentication tests
├── test_users.py           # User management tests
├── test_foods.py           # Food search and retrieval tests
├── test_food_log.py        # Food logging tests
├── test_dashboard.py       # Dashboard analytics tests
├── test_recommendations.py # AI recommendations tests
├── test_recipe.py          # Recipe parsing tests
└── test_rate_limiting.py   # Rate limiting tests
```

### Database Configuration
- **Testing**: SQLite in-memory database for fast, isolated tests
- **Production**: PostgreSQL for robust data storage
- **Auto-switching**: Based on `DATABASE_URL` environment variable

### Test Features
- **Isolated Tests**: Each test uses fresh database state
- **Authentication Testing**: JWT token generation and validation
- **API Endpoint Testing**: All REST endpoints covered
- **Edge Case Testing**: Invalid inputs, unauthorized access, rate limiting
- **Mock Data**: Realistic test data for comprehensive coverage

### Running Backend Tests
```bash
cd backend
uv run pytest tests/ -v                    # Run all tests
uv run pytest tests/test_auth.py -v        # Run specific test file
uv run pytest tests/ --cov=app             # Run with coverage
```

### Test Coverage Areas
- ✅ User registration and authentication
- ✅ Profile management
- ✅ Food search and retrieval
- ✅ Food logging functionality
- ✅ Dashboard analytics
- ✅ AI-powered recommendations
- ✅ Recipe parsing
- ✅ Rate limiting protection
- ✅ Error handling and edge cases

## Frontend Testing

### Test Structure
```
frontend/src/
├── setupTests.js                    # Test configuration
├── context/__tests__/
│   └── AuthContext.test.js         # Authentication context tests
├── pages/__tests__/
│   ├── Login.test.js               # Login component tests
│   └── Register.test.js            # Registration component tests
└── services/__tests__/
    └── api.test.js                 # API service tests
```

### Test Features
- **Component Testing**: React components with user interactions
- **Context Testing**: Authentication state management
- **API Testing**: Service layer with mocked responses
- **User Event Testing**: Form submissions, navigation
- **Error Handling**: Network errors, validation errors

### Running Frontend Tests
```bash
cd frontend
npm test                            # Run all tests
npm run test:ui                     # Run with UI interface
npm test -- --coverage             # Run with coverage
```

### Test Coverage Areas
- ✅ Authentication flow (login/register)
- ✅ Form validation and submission
- ✅ API service integration
- ✅ Context state management
- ✅ Error handling and user feedback
- ✅ Navigation and routing

## Test Data and Fixtures

### Backend Fixtures
```python
# User test data
test_user_data = {
    "email": "test@example.com",
    "password": "testpassword123"
}

# Profile test data
test_profile_data = {
    "birth_date": "1990-01-01",
    "gender": "male",
    "height_cm": 175,
    "weight_kg": 70,
    "activity_level": "moderate"
}
```

### Frontend Mocks
- **API calls**: Mocked with realistic responses
- **LocalStorage**: Mocked for token management
- **Browser APIs**: IntersectionObserver, matchMedia mocked

## Edge Cases Tested

### Authentication
- Invalid email formats
- Weak passwords
- Duplicate registrations
- Invalid OTP codes
- Expired tokens
- Unauthorized access attempts

### Data Validation
- Negative values (weight, height)
- Invalid date formats
- Missing required fields
- SQL injection attempts
- XSS prevention

### Rate Limiting
- Exceeding request limits
- Different IP addresses
- Time window resets
- Endpoint-specific limits

### Error Scenarios
- Network failures
- Database connection issues
- Invalid API responses
- Malformed JSON data

## Continuous Integration

### GitHub Actions (Recommended)
```yaml
name: Tests
on: [push, pull_request]
jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - run: cd backend && uv sync
      - run: cd backend && uv run pytest tests/ --cov=app
  
  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: cd frontend && npm install
      - run: cd frontend && npm test -- --coverage
```

## Performance Testing

### Load Testing (Recommended Tools)
- **Locust**: For API load testing
- **Artillery**: For HTTP load testing
- **k6**: For performance testing

### Database Performance
- **Query optimization**: Index usage analysis
- **Connection pooling**: Concurrent request handling
- **Memory usage**: SQLite vs PostgreSQL comparison

## Security Testing

### Automated Security Scans
- **Bandit**: Python security linting
- **Safety**: Dependency vulnerability scanning
- **npm audit**: Frontend dependency security

### Manual Security Testing
- **SQL Injection**: Parameterized queries validation
- **XSS Prevention**: Input sanitization testing
- **CSRF Protection**: Token validation
- **Rate Limiting**: DDoS protection verification

## Test Environment Setup

### Local Development
1. **Backend**: SQLite database (automatic)
2. **Frontend**: Mock API responses
3. **Integration**: Local backend + frontend

### Staging Environment
1. **Backend**: PostgreSQL database
2. **Frontend**: Staging API endpoints
3. **E2E Testing**: Full user workflows

### Production Testing
1. **Smoke Tests**: Critical path verification
2. **Health Checks**: Service availability
3. **Performance Monitoring**: Response times

## Best Practices

### Test Writing
- **Descriptive Names**: Clear test purpose
- **Single Responsibility**: One assertion per test
- **Independent Tests**: No test dependencies
- **Realistic Data**: Production-like test data

### Test Maintenance
- **Regular Updates**: Keep tests current with features
- **Flaky Test Fixes**: Address intermittent failures
- **Coverage Goals**: Maintain >80% code coverage
- **Documentation**: Update test docs with changes

## Troubleshooting

### Common Issues
1. **Database Connection**: Check DATABASE_URL
2. **Rate Limiting**: Tests hitting limits
3. **Mock Failures**: API response mismatches
4. **Async Issues**: Proper await/async handling

### Debug Commands
```bash
# Backend debugging
cd backend && uv run pytest tests/ -v -s --pdb

# Frontend debugging
cd frontend && npm test -- --verbose

# Database inspection
sqlite3 test.db ".tables"
```

This comprehensive testing setup ensures code quality, prevents regressions, and provides confidence in deployments.
