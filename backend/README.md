# Fitness Tracker Backend

FastAPI backend with email verification for user registration.

## SMTP Email Setup

To enable email verification, configure these environment variables in `.env`:

```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=your-email@gmail.com
```

### Gmail Setup:
1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password: Google Account → Security → App passwords
3. Use the app password (not your regular password) in `SMTP_PASSWORD`

### Other Email Providers:
- **Outlook**: `smtp-mail.outlook.com:587`
- **Yahoo**: `smtp.mail.yahoo.com:587`
- **Custom SMTP**: Use your provider's settings

## Development Mode

If SMTP is not configured, the system will:
- Print OTP to console for development
- Still allow registration/verification to work
- Return OTP in API response (remove in production)

## Usage

1. User registers → OTP sent via email
2. User enters OTP → Account activated
3. User can login with JWT tokens
