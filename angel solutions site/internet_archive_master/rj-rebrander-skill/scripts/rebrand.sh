#!/bin/bash

# ============================================
# RJ Business Solutions - Template Rebrander
# ============================================
# 
# Usage: ./rebrand.sh [options]
# 
# Options:
#   --preview     Show what would be changed without making changes
#   --dir PATH    Target directory (default: current directory)
#   --backup      Create backup before changes
#   --old-brand   Original brand name to replace (default: auto-detect)
#   --help        Show this help message
#
# ============================================

set -e

# RJ Business Solutions Brand Configuration
RJ_NAME="RJ Business Solutions"
RJ_SHORT_NAME="RJ Business"
RJ_FOUNDER="Rick Jefferson"
RJ_EMAIL="support@rjbusinesssolutions.org"
RJ_WEBSITE="https://rjbusinesssolutions.org"
RJ_ADDRESS="1342 NM 333, Tijeras, New Mexico 87059"
RJ_LOGO="https://storage.googleapis.com/msgsndr/qQnxRHDtyx0uydPd5sRl/media/67eb83c5e519ed689430646b.jpeg"
RJ_LINKEDIN="https://www.linkedin.com/in/rick-jefferson-314998235"
RJ_TIKTOK="https://www.tiktok.com/@rick_jeff_solution"
RJ_TWITTER="https://twitter.com/ricksolutions1"
RJ_PRIMARY_COLOR="#2563eb"
RJ_SECONDARY_COLOR="#0ea5e9"
RJ_TAGLINE="AI-powered systems for businesses ready to scale."
RJ_DESCRIPTION="RJ Business Solutions builds AI-powered automation, credit technology, funnels, client portals, CRM workflows, and growth systems for businesses ready to scale."

# Script settings
PREVIEW_MODE=false
TARGET_DIR="."
CREATE_BACKUP=false
OLD_BRAND=""
CURRENT_YEAR=$(date +%Y)

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --preview)
            PREVIEW_MODE=true
            shift
            ;;
        --dir)
            TARGET_DIR="$2"
            shift 2
            ;;
        --backup)
            CREATE_BACKUP=true
            shift
            ;;
        --old-brand)
            OLD_BRAND="$2"
            shift 2
            ;;
        --help)
            echo "RJ Business Solutions - Template Rebrander"
            echo ""
            echo "Usage: ./rebrand.sh [options]"
            echo ""
            echo "Options:"
            echo "  --preview     Show what would be changed without making changes"
            echo "  --dir PATH    Target directory (default: current directory)"
            echo "  --backup      Create backup before changes"
            echo "  --old-brand   Original brand name to replace"
            echo "  --help        Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Auto-detect old brand name
detect_brand() {
    log_info "Detecting existing brand name..."
    
    # Common patterns to look for
    local brands=$(grep -rhoE '(Aivora|Starter|Template|Company|Agency|Brand)' \
        --include="*.html" --include="*.tsx" --include="*.jsx" \
        "$TARGET_DIR" 2>/dev/null | sort | uniq -c | sort -rn | head -1 | awk '{print $2}')
    
    if [[ -n "$brands" ]]; then
        OLD_BRAND="$brands"
        log_info "Detected brand: $OLD_BRAND"
    else
        log_warning "Could not auto-detect brand. Using 'Aivora' as default."
        OLD_BRAND="Aivora"
    fi
}

# Create backup
create_backup() {
    local backup_dir="${TARGET_DIR}_backup_$(date +%Y%m%d_%H%M%S)"
    log_info "Creating backup at $backup_dir"
    cp -r "$TARGET_DIR" "$backup_dir"
    log_success "Backup created: $backup_dir"
}

# Find brand references
find_brand_references() {
    log_info "Scanning for brand references..."
    echo ""
    
    echo -e "${YELLOW}=== Company Name References ===${NC}"
    grep -rn "$OLD_BRAND" --include="*.{tsx,ts,jsx,js,html,css,json,md}" "$TARGET_DIR" 2>/dev/null | head -20 || echo "None found"
    
    echo ""
    echo -e "${YELLOW}=== Logo References ===${NC}"
    grep -rn "logo\|Logo" --include="*.{tsx,ts,jsx,js}" "$TARGET_DIR" 2>/dev/null | head -10 || echo "None found"
    
    echo ""
    echo -e "${YELLOW}=== Copyright References ===${NC}"
    grep -rn "copyright\|Copyright\|©" --include="*.{tsx,ts,jsx,js,html}" "$TARGET_DIR" 2>/dev/null | head -10 || echo "None found"
    
    echo ""
    echo -e "${YELLOW}=== Contact Info References ===${NC}"
    grep -rn "@.*\.com\|@.*\.org\|tel:\|mailto:" --include="*.{tsx,ts,jsx,js,html}" "$TARGET_DIR" 2>/dev/null | head -10 || echo "None found"
    
    echo ""
    echo -e "${YELLOW}=== Color Pattern References ===${NC}"
    grep -rn "#00ff\|#0ff\|#00FF" --include="*.{css,scss,tsx,ts}" "$TARGET_DIR" 2>/dev/null | head -10 || echo "None found"
}

# Perform replacements
perform_replacements() {
    log_info "Performing brand replacements..."
    
    # Text replacements array
    declare -A replacements=(
        ["$OLD_BRAND"]="$RJ_NAME"
        ["${OLD_BRAND,,}"]="${RJ_NAME,,}"  # lowercase
        ["${OLD_BRAND^^}"]="${RJ_NAME^^}"  # uppercase
        ["Copyright © 2025"]="© $CURRENT_YEAR"
        ["Copyright © 2024"]="© $CURRENT_YEAR"
        ["© 2025"]="© $CURRENT_YEAR"
        ["© 2024"]="© $CURRENT_YEAR"
    )
    
    # File extensions to process
    local extensions="tsx,ts,jsx,js,html,css,scss,json,md"
    
    for old in "${!replacements[@]}"; do
        local new="${replacements[$old]}"
        log_info "Replacing: '$old' -> '$new'"
        
        if [[ "$PREVIEW_MODE" == true ]]; then
            grep -rn "$old" --include="*.{$extensions}" "$TARGET_DIR" 2>/dev/null | head -5 || true
        else
            find "$TARGET_DIR" -type f \( -name "*.tsx" -o -name "*.ts" -o -name "*.jsx" -o -name "*.js" -o -name "*.html" -o -name "*.css" -o -name "*.scss" -o -name "*.json" -o -name "*.md" \) -exec sed -i "s|$old|$new|g" {} \; 2>/dev/null || true
        fi
    done
}

# Update specific files
update_manifest() {
    local manifest="$TARGET_DIR/public/manifest.json"
    if [[ -f "$manifest" ]]; then
        log_info "Updating manifest.json..."
        if [[ "$PREVIEW_MODE" == false ]]; then
            cat > "$manifest" << EOF
{
  "short_name": "$RJ_SHORT_NAME",
  "name": "$RJ_NAME",
  "description": "$RJ_TAGLINE",
  "icons": [
    {
      "src": "favicon.ico",
      "sizes": "64x64 32x32 24x24 16x16",
      "type": "image/x-icon"
    },
    {
      "src": "logo192.png",
      "type": "image/png",
      "sizes": "192x192"
    },
    {
      "src": "logo512.png",
      "type": "image/png",
      "sizes": "512x512"
    }
  ],
  "start_url": ".",
  "display": "standalone",
  "theme_color": "$RJ_PRIMARY_COLOR",
  "background_color": "#ffffff"
}
EOF
            log_success "Updated manifest.json"
        fi
    fi
}

update_package_json() {
    local package="$TARGET_DIR/package.json"
    if [[ -f "$package" ]]; then
        log_info "Updating package.json name..."
        if [[ "$PREVIEW_MODE" == false ]]; then
            # Update name field
            sed -i 's/"name": ".*"/"name": "rj-business-solutions"/g' "$package"
            # Update homepage if exists
            sed -i "s|\"homepage\": \".*\"|\"homepage\": \"$RJ_WEBSITE\"|g" "$package"
            log_success "Updated package.json"
        fi
    fi
}

# Main execution
main() {
    echo ""
    echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║     RJ Business Solutions - Template Rebrander             ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    if [[ "$PREVIEW_MODE" == true ]]; then
        log_warning "PREVIEW MODE - No changes will be made"
    fi
    
    log_info "Target directory: $TARGET_DIR"
    
    # Detect brand if not specified
    if [[ -z "$OLD_BRAND" ]]; then
        detect_brand
    fi
    
    # Create backup if requested
    if [[ "$CREATE_BACKUP" == true ]]; then
        create_backup
    fi
    
    # Find references
    find_brand_references
    
    echo ""
    echo -e "${YELLOW}Press Enter to continue with replacements (or Ctrl+C to cancel)...${NC}"
    read -r
    
    # Perform replacements
    perform_replacements
    
    # Update specific files
    update_manifest
    update_package_json
    
    echo ""
    log_success "Rebranding complete!"
    echo ""
    
    log_info "Next steps:"
    echo "  1. Replace logo image files with RJ Business Solutions logo"
    echo "  2. Update CSS color variables if not already done"
    echo "  3. Test all pages to verify branding"
    echo "  4. Run: grep -rn '$OLD_BRAND' . to check for remaining references"
    echo ""
}

main
