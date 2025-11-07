# GitHub Secrets Setup

## Required Environment Variables for Backend Testing

### ✅ **No Secrets Required for Testing!**

The backend tests now work without any GitHub secrets. All required environment variables have default values:

- `SECRET_KEY` → defaults to `"fallback-secret-key-for-testing"`
- `ACCESS_TOKEN_EXPIRE_MINUTES` → defaults to `30`
- `GEMINI_API_KEY` → defaults to `"test-api-key-for-ci"`
- `DATABASE_URL` → uses SQLite for testing

### ☁️ **For AWS Lambda Deployment (Optional)**
```
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
```

### 🚀 **For Vercel Deployment (Optional)**
```
VERCEL_TOKEN=your-vercel-token
VERCEL_ORG_ID=your-vercel-org-id
VERCEL_PROJECT_ID=your-vercel-project-id
```

### 📊 **For Coverage Reporting (Optional)**
```
CODECOV_TOKEN=your-codecov-token
```

## Current Pipeline Status

**Without any secrets:**
- ✅ Backend tests run successfully
- ✅ Security scans work
- ✅ Frontend builds
- ❌ Deployment steps are skipped

**With deployment secrets:**
- ✅ All of the above
- ✅ Automatic deployment to AWS Lambda
- ✅ Automatic deployment to Vercel

## How to Add Secrets (Optional)

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add each secret with the name and value

**The pipeline works perfectly without any secrets for testing and CI purposes!**
