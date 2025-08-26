#!/usr/bin/env python3
"""
SMTP2Go Test Script for UCMe

This script tests your SMTP2Go configuration by sending a test verification email.
Run this after setting up your .env file to verify everything works.

Usage:
    python test_smtp.py [email]
    
Example:
    python test_smtp.py test@example.com
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_smtp_configuration():
    """Test SMTP configuration and send a test email"""
    
    print("🔧 Testing SMTP Configuration...")
    print("=" * 50)
    
    # Check required environment variables
    required_vars = ['SMTP_HOST', 'SMTP_USER', 'SMTP_PASSWORD']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("Please check your .env file and ensure all SMTP variables are set.")
        return False
    
    # Display current configuration
    print("✅ Environment variables found:")
    print(f"   SMTP_HOST: {os.getenv('SMTP_HOST')}")
    print(f"   SMTP_PORT: {os.getenv('SMTP_PORT', '587')}")
    print(f"   SMTP_USER: {os.getenv('SMTP_USER')}")
    print(f"   SMTP_TLS: {os.getenv('SMTP_TLS', 'true')}")
    print(f"   SMTP_SSL: {os.getenv('SMTP_SSL', 'false')}")
    print(f"   APP_NAME: {os.getenv('APP_NAME', 'UCMe')}")
    print()
    
    # Test email sending
    try:
        from utils.auth import sendVerificationEmail
        
        # Get test email from command line or use default
        test_email = sys.argv[1] if len(sys.argv) > 1 else "test@example.com"
        test_code = "123456"
        
        print(f"📧 Sending test email to: {test_email}")
        print(f"🔑 Test verification code: {test_code}")
        print()
        
        result = sendVerificationEmail(test_email, test_code)
        
        if result:
            print("✅ Test email sent successfully!")
            print(f"📬 Check your inbox at: {test_email}")
            print("💡 If you don't see the email, check your spam folder")
        else:
            print("❌ Failed to send test email")
            print("🔍 Check the logs above for error details")
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're running this script from the backend directory")
        return False
    except Exception as e:
        print(f"❌ Error during email test: {e}")
        return False
    
    return True

def show_help():
    """Show help information"""
    print("UCMe SMTP2Go Test Script")
    print("=" * 30)
    print()
    print("Usage:")
    print("  python test_smtp.py [email]")
    print()
    print("Examples:")
    print("  python test_smtp.py                    # Use default test@example.com")
    print("  python test_smtp.py your@email.com     # Test with specific email")
    print()
    print("Prerequisites:")
    print("  1. Copy env.example to .env")
    print("  2. Configure SMTP2Go credentials in .env")
    print("  3. Install requirements: pip install -r requirements.txt")
    print()
    print("For detailed setup instructions, see: SMTP2GO_SETUP.md")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help', 'help']:
        show_help()
    else:
        success = test_smtp_configuration()
        sys.exit(0 if success else 1) 