# CI/CD Workflows

## Overview

This repository uses GitHub Actions for continuous integration and deployment with comprehensive testing, security scanning, and performance monitoring.

## Workflows

### 1. CI/CD Pipeline (`ci-cd.yml`)
**Triggers**: Push to master/main, Pull Requests

**Jobs**:
- **Backend Tests**: Run pytest with coverage, PostgreSQL service
- **Frontend Build**: Build React app, upload artifacts
- **Deploy Backend**: Deploy to AWS Lambda (master only)
- **Deploy Frontend**: Deploy to Vercel (master only)
- **Security Scan**: Bandit + Safety security analysis
- **Performance Test**: k6 load testing post-deployment

### 2. Pull Request Checks (`pr-checks.yml`)
**Triggers**: Pull Requests to master/main

**Jobs**:
- **Code Quality**: Black, Flake8, isort, ESLint
- **Test Coverage**: Pytest with 70% minimum coverage
- **Coverage Comments**: Automatic PR coverage reports

### 3. Staging Deployment (`deploy-staging.yml`)
**Triggers**: Push to develop/staging branches

**Jobs**:
- **Deploy Staging**: Deploy to staging environment
- **Smoke Tests**: Basic health checks post-deployment

## Required Secrets

### AWS Deployment
```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
```

### Vercel Deployment
```
VERCEL_TOKEN
VERCEL_ORG_ID
VERCEL_PROJECT_ID
```

### Environment Variables
```
STAGING_SECRET_KEY
STAGING_GEMINI_API_KEY
STAGING_DATABASE_URL
```

## Workflow Status

Add these badges to your README:

```markdown
![CI/CD](https://github.com/akash2704/NutriTracker/workflows/CI/CD%20Pipeline/badge.svg)
![Tests](https://github.com/akash2704/NutriTracker/workflows/Pull%20Request%20Checks/badge.svg)
```

## Features

### ✅ Automated Testing
- Backend: pytest with SQLite/PostgreSQL
- Coverage: Minimum 70% required
- Security: Bandit + Safety scans

### ✅ Code Quality
- Python: Black, Flake8, isort
- JavaScript: ESLint
- Automated formatting checks

### ✅ Deployment
- **Production**: AWS Lambda + Vercel
- **Staging**: Separate staging environment
- **Rollback**: Manual trigger available

### ✅ Monitoring
- Performance testing with k6
- Health checks post-deployment
- Coverage reporting on PRs

### ✅ Security
- Dependency vulnerability scanning
- Code security analysis
- Environment-specific secrets

## Usage

### Development Workflow
1. Create feature branch
2. Make changes
3. Push → PR checks run automatically
4. Merge to master → Full CI/CD pipeline

### Emergency Deployment
```bash
# Manual trigger via GitHub Actions UI
# Or use GitHub CLI
gh workflow run ci-cd.yml
```

### Local Testing
```bash
# Backend
cd backend
uv run pytest tests/ -v --cov=app

# Frontend
cd frontend
npm run lint
npm run build
```

This setup ensures code quality, prevents regressions, and provides reliable deployments with comprehensive monitoring.
