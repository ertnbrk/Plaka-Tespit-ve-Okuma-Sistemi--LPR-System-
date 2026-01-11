#!/bin/bash

# Git Cleanup Script
# Removes files from git tracking that should be ignored

echo "============================================"
echo "  Git Repository Cleanup Script"
echo "============================================"
echo ""
echo "This script will remove ignored files from git tracking"
echo "Files will remain on disk but won't be committed"
echo ""

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Not a git repository!"
    echo "Run: git init"
    exit 1
fi

echo "Current status:"
git status --short | head -n 10
echo ""

read -p "Do you want to proceed with cleanup? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Cleanup cancelled."
    exit 0
fi

echo ""
echo "→ Removing debug/output files from git..."

# Remove debug and output files
git rm --cached -f db_test_output.txt 2>/dev/null && echo "  ✓ Removed db_test_output.txt"
git rm --cached -f debug_result.txt 2>/dev/null && echo "  ✓ Removed debug_result.txt"
git rm --cached -f dns_debug_out.txt 2>/dev/null && echo "  ✓ Removed dns_debug_out.txt"
git rm --cached -f dns_debug_result_utf8.txt 2>/dev/null && echo "  ✓ Removed dns_debug_result_utf8.txt"

echo ""
echo "→ Removing Python cache directories..."

# Remove __pycache__ directories
find . -name "__pycache__" -type d | while read dir; do
    git rm -r --cached "$dir" 2>/dev/null && echo "  ✓ Removed $dir"
done

echo ""
echo "→ Checking for .env file..."

# Check if .env is tracked
if git ls-files --error-unmatch .env > /dev/null 2>&1; then
    echo "  ⚠️  WARNING: .env file is tracked in git!"
    echo "  This file contains secrets and should NOT be committed!"
    read -p "Remove .env from git? (yes/no): " remove_env
    if [ "$remove_env" == "yes" ]; then
        git rm --cached .env && echo "  ✓ Removed .env from git"
        echo "  ℹ️  File still exists on disk"
    fi
else
    echo "  ✓ .env is not tracked (good!)"
fi

echo ""
echo "→ Checking for large model files..."

# Check for large .pt files
find . -name "*.pt" -type f 2>/dev/null | while read file; do
    if git ls-files --error-unmatch "$file" > /dev/null 2>&1; then
        echo "  ⚠️  Found tracked model file: $file"
        read -p "Remove from git? (yes/no): " remove_model
        if [ "$remove_model" == "yes" ]; then
            git rm --cached "$file" && echo "  ✓ Removed $file from git"
        fi
    fi
done

echo ""
echo "============================================"
echo "  Cleanup Complete!"
echo "============================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Review changes:"
echo "   git status"
echo ""
echo "2. Commit the cleanup:"
echo "   git commit -m \"Remove ignored files from git tracking\""
echo ""
echo "3. Add new files (respecting .gitignore):"
echo "   git add ."
echo "   git commit -m \"Add backend application\""
echo ""
echo "4. Push to GitHub:"
echo "   git push origin main"
echo ""
