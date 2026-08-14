#!/bin/bash

#######################################################################
# Internet Archive Ultimate Master System
# Deployment Script
# 
# Author: RJ PROMETHEUS APEX
# Company: RJ Business Solutions
# Date: 2026-07-11
#######################################################################

set -e  # Exit on error

echo "================================================================"
echo "Internet Archive Ultimate Master System - Deployment"
echo "================================================================"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check Python version
print_info "Checking Python version..."
python_version=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+')
required_version="3.10"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    print_error "Python 3.10+ required (found $python_version)"
    exit 1
fi

print_success "Python $python_version detected"

# Create virtual environment
print_info "Creating virtual environment..."
if [ -d "venv" ]; then
    print_warning "Virtual environment already exists, skipping..."
else
    python3 -m venv venv
    print_success "Virtual environment created"
fi

# Activate virtual environment
print_info "Activating virtual environment..."
source venv/bin/activate
print_success "Virtual environment activated"

# Upgrade pip
print_info "Upgrading pip..."
pip install --upgrade pip --quiet
print_success "Pip upgraded"

# Install dependencies
print_info "Installing dependencies..."
pip install -r requirements.txt --quiet
print_success "Dependencies installed"

# Install package in development mode
print_info "Installing package..."
pip install -e . --quiet
print_success "Package installed"

# Create necessary directories
print_info "Creating directories..."
mkdir -p downloads
mkdir -p output
mkdir -p logs
print_success "Directories created"

# Set permissions
print_info "Setting permissions..."
chmod +x cli/ia_cli.py
chmod +x deploy.sh
print_success "Permissions set"

# Run basic test
print_info "Running basic tests..."
python3 -c "from core.ia_client import InternetArchiveClient; client = InternetArchiveClient(); print('✅ Client initialized successfully')"
print_success "Tests passed"

echo ""
echo "================================================================"
echo "✅ DEPLOYMENT COMPLETE!"
echo "================================================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Configure credentials:"
echo "   ${BLUE}ia configure${NC}"
echo "   Or set environment variables:"
echo "   ${BLUE}export IA_ACCESS_KEY='your_key'${NC}"
echo "   ${BLUE}export IA_SECRET_KEY='your_secret'${NC}"
echo ""
echo "2. Run examples:"
echo "   ${BLUE}python3 examples/basic_usage.py${NC}"
echo ""
echo "3. Use CLI:"
echo "   ${BLUE}ia search 'collection:nasa'${NC}"
echo "   ${BLUE}ia --help${NC}"
echo ""
echo "4. Read documentation:"
echo "   ${BLUE}cat README.md${NC}"
echo "   ${BLUE}cat docs/API_REFERENCE.md${NC}"
echo ""
echo "Get your API keys at: ${BLUE}https://archive.org/account/s3.php${NC}"
echo ""
echo "================================================================"
