#!/bin/bash
# Setup script for local development of Carved Rock Flask app

set -e  # Exit on any error

echo "🏔️ Carved Rock Fitness - Setup Script"
echo "======================================="
echo ""

# Check if Python 3.11+ is installed
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python $python_version found"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
echo "✓ pip upgraded"
echo ""

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt > /dev/null 2>&1
echo "✓ Dependencies installed"
echo ""

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit .env with your configuration"
else
    echo "✓ .env file already exists"
fi
echo ""

# Initialize database
echo "Initializing database..."
python3 -c "from app import app, init_db; init_db(app); print('✓ Database initialized')"
echo ""

echo "✅ Setup complete!"
echo ""
echo "To start the application, run:"
echo "  source venv/bin/activate"
echo "  flask run"
echo ""
echo "Or use Docker Compose:"
echo "  docker-compose up"
echo ""
echo "Application will be available at: http://localhost:5000"
echo "Admin dashboard: http://localhost:5000/admin/login"
echo ""
