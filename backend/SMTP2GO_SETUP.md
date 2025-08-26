# SMTP2Go Setup Guide for UCMe

This guide will help you configure SMTP2Go to send verification emails for the UCMe matchmaking application.

## 🚀 Quick Setup

### 1. Create SMTP2Go Account
1. Go to [SMTP2Go.com](https://www.smtp2go.com/)
2. Sign up for a free account (1000 emails/month free)
3. Verify your email address

### 2. Get Your Credentials
1. Log into your SMTP2Go dashboard
2. Go to **Settings** → **API Keys**
3. Note down your:
   - **Username** (usually your email)
   - **Password** (API key)

### 3. Configure Environment Variables
Copy these settings to your `.env` file:

```bash
# SMTP2Go Configuration
SMTP_HOST=mail.smtp2go.com
SMTP_PORT=2525
SMTP_USER=your-email@example.com
SMTP_PASSWORD=your-api-key-here
SMTP_TLS=true
SMTP_SSL=false
APP_NAME=UCMe
```

## 🔧 Port Options

SMTP2Go supports multiple ports. Choose based on your needs:

| Port | Protocol | Security | Use Case |
|------|----------|----------|----------|
| **2525** | SMTP | TLS | **Recommended** - Most reliable |
| **587** | SMTP | TLS | Standard submission port |
| **465** | SMTP | SSL | Legacy SSL port |
| **25** | SMTP | None | Not recommended (no encryption) |

## 📧 Email Templates

The application automatically sends verification emails with this format:

**Subject:** `Your UCMe Verification Code`

**Content:**
```html
<h2>Welcome to UCMe!</h2>
<p>Your verification code is: <strong>123456</strong></p>
<p>This code will expire in 5 minutes.</p>
<p>Please do not share this code with anyone.</p>
```

## 🧪 Testing Your Setup

### 1. Test Email Sending
```bash
cd backend
python -c "
from utils.auth import sendVerificationEmail
result = sendVerificationEmail('test@example.com', '123456')
print(f'Email sent: {result}')
"
```

### 2. Check Logs
Look for these messages in your backend console:
- ✅ `Verification email sent successfully to test@example.com`
- ❌ `Failed to send email to test@example.com. Status: XXX`

## 🚨 Troubleshooting

### Common Issues

#### 1. Authentication Failed
```
Error: Authentication failed
```
**Solution:** Check your username and password in `.env`

#### 2. Connection Timeout
```
Error: Connection timeout
```
**Solution:** Try different ports (2525, 587, 465)

#### 3. TLS/SSL Issues
```
Error: SSL/TLS connection failed
```
**Solution:** 
- For port 2525: Set `SMTP_TLS=true`, `SMTP_SSL=false`
- For port 465: Set `SMTP_TLS=false`, `SMTP_SSL=true`
- For port 587: Set `SMTP_TLS=true`, `SMTP_SSL=false`

### Debug Mode
Enable detailed logging by setting in your `.env`:
```bash
LOG_LEVEL=DEBUG
```

## 📊 Monitoring

### SMTP2Go Dashboard
- Monitor email delivery rates
- View bounce reports
- Check API usage

### Application Logs
The application logs all email operations:
- Successful sends
- Failed attempts
- Fallback to console logging

## 🔒 Security Best Practices

1. **Never commit `.env` files** to version control
2. **Use API keys** instead of account passwords
3. **Rotate API keys** regularly
4. **Monitor for unusual activity** in SMTP2Go dashboard

## 💰 Cost Considerations

- **Free Tier**: 1,000 emails/month
- **Paid Plans**: Starting at $10/month for 10,000 emails
- **Enterprise**: Custom pricing for high volume

## 📞 Support

- **SMTP2Go Support**: [support@smtp2go.com](mailto:support@smtp2go.com)
- **UCMe Issues**: Check the main README or create an issue

## ✅ Verification Checklist

- [ ] SMTP2Go account created
- [ ] API credentials obtained
- [ ] Environment variables configured
- [ ] Test email sent successfully
- [ ] Verification codes received in email
- [ ] Application working with email verification

---

**Need help?** Check the main `LOCAL_DEVELOPMENT.md` file or create an issue in the repository. 