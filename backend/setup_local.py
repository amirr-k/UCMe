#!/usr/bin/env python3
"""
Local Development Setup Script for UCMe Backend
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_dependencies():
    """Install Python dependencies"""
    return run_command("pip install -r requirements.txt", "Installing Python dependencies")

def create_env_file():
    """Create .env file from template"""
    if os.path.exists('.env'):
        print("✅ .env file already exists")
        return True
    
    if not os.path.exists('env.example'):
        print("❌ env.example file not found")
        return False
    
    # Generate secret key
    print("🔑 Generating secret key...")
    try:
        result = subprocess.run("python generate_secret_key.py", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Secret key generated")
        else:
            print("⚠️  Could not generate secret key automatically")
    except:
        print("⚠️  Could not generate secret key automatically")
    
    # Copy env.example to .env
    try:
        with open('env.example', 'r') as f:
            content = f.read()
        
        with open('.env', 'w') as f:
            f.write(content)
        
        print("✅ .env file created from template")
        print("⚠️  IMPORTANT: Edit .env file with your actual database and configuration")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def create_uploads_directory():
    """Create uploads directory for images"""
    uploads_dir = "uploads/images"
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)
        print(f"✅ Created {uploads_dir} directory")
    else:
        print(f"✅ {uploads_dir} directory already exists")

def main():
    """Main setup function"""
    print("🚀 UCMe Backend Local Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Setup failed at dependency installation")
        return
    
    # Create environment file
    if not create_env_file():
        print("❌ Setup failed at environment file creation")
        return
    
    # Create uploads directory
    create_uploads_directory()
    
    print("\n🎉 Setup completed successfully!")
    print("\n📝 Next steps:")
    print("1. Edit .env file with your database configuration")
    print("2. Set up PostgreSQL database (see README_CONFIG.md)")
    print("3. Run: python -m uvicorn main:app --reload")
    print("4. Open http://localhost:8000 in your browser")

if __name__ == "__main__":
    main() 