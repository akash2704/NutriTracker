# GitHub Secrets Setup

## Required Secrets for CI/CD Pipeline

### 🔧 **For Tests (Optional - uses defaults if not set)**
```
# These are optional - tests will use default values if not provided
SECRET_KEY=your-test-secret-key
GEMINI_API_KEY=your-test-gemini-key
```

### ☁️ **For AWS Lambda Deployment (Required for production deployment)**
```
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
```

### 🚀 **For Vercel Deployment (Required for frontend deployment)**
```
VERCEL_TOKEN=your-vercel-token
VERCEL_ORG_ID=your-vercel-org-id
VERCEL_PROJECT_ID=your-vercel-project-id
```

### 📊 **For Coverage Reporting (Optional)**
```
CODECOV_TOKEN=your-codecov-token
```

## How to Add Secrets

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add each secret with the name and value

## Getting the Values

### AWS Credentials
1. Go to AWS IAM Console
2. Create a user with Lambda deployment permissions
3. Generate access keys

### Vercel Credentials
1. Go to Vercel Dashboard → Settings → Tokens
2. Create a new token
3. Get Org ID and Project ID from project settings

### Codecov Token
1. Go to codecov.io
2. Connect your GitHub repository
3. Get the upload token

## Minimal Setup (Tests Only)

**For just running tests without deployment, you don't need any secrets!**

The pipeline will:
- ✅ Run all backend tests with SQLite
- ✅ Run security scans
- ✅ Build frontend
- ❌ Skip deployment steps (no secrets = no deployment)

## Production Setup

Add all secrets above for full CI/CD with:
- ✅ Automated testing
- ✅ Security scanning  
- ✅ AWS Lambda deployment
- ✅ Vercel frontend deployment
- ✅ Coverage reporting
