#!/usr/bin/env python3
"""
Quick validation script for Hugging Face Spaces deployment package.
Run this before deploying to catch common issues.
"""

import os
import sys
from pathlib import Path

def check_file_exists(filepath: str, required: bool = True) -> bool:
    """Check if a file exists."""
    exists = os.path.isfile(filepath)
    status = "✓" if exists else ("✗" if required else "⚠")
    req_str = "(required)" if required else "(optional)"
    print(f"{status} {filepath} {req_str}")
    return exists

def check_file_content(filepath: str, search_terms: list) -> bool:
    """Check if file contains required content."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        missing = []
        for term in search_terms:
            if term not in content:
                missing.append(term)
        
        if missing:
            print(f"  ⚠ Missing content: {', '.join(missing)}")
            return False
        return True
    except Exception as e:
        print(f"  ✗ Error reading file: {e}")
        return False

def main():
    print("=" * 60)
    print("Hugging Face Spaces Deployment Package Validation")
    print("=" * 60)
    print()
    
    # Change to huggingface directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    all_checks_passed = True
    
    # Check required files
    print("Checking required files...")
    required_files = [
        "app.py",
        "sam_audio_integration.py",
        "requirements.txt",
        "packages.txt",
        "README.md",
    ]
    
    for filepath in required_files:
        if not check_file_exists(filepath, required=True):
            all_checks_passed = False
    
    print()
    
    # Check optional files
    print("Checking optional files...")
    optional_files = [
        "DEPLOYMENT.md",
        "PACKAGE_INFO.md",
        ".env.example",
        ".gitignore",
    ]
    
    for filepath in optional_files:
        check_file_exists(filepath, required=False)
    
    print()
    
    # Validate README.md YAML header
    print("Validating README.md...")
    if os.path.isfile("README.md"):
        required_yaml = ["title:", "emoji:", "sdk: gradio", "app_file: app.py"]
        if check_file_content("README.md", required_yaml):
            print("  ✓ YAML header looks good")
        else:
            print("  ✗ YAML header missing required fields")
            all_checks_passed = False
    
    print()
    
    # Validate requirements.txt
    print("Validating requirements.txt...")
    if os.path.isfile("requirements.txt"):
        required_packages = ["gradio", "numpy", "librosa", "soundfile"]
        if check_file_content("requirements.txt", required_packages):
            print("  ✓ Core dependencies present")
        else:
            print("  ✗ Missing core dependencies")
            all_checks_passed = False
    
    print()
    
    # Check Python imports in app.py
    print("Validating app.py imports...")
    if os.path.isfile("app.py"):
        required_imports = [
            "import gradio",
            "from sam_audio_integration import",
        ]
        if check_file_content("app.py", required_imports):
            print("  ✓ Required imports present")
        else:
            print("  ✗ Missing required imports")
            all_checks_passed = False
    
    print()
    
    # Check for common issues
    print("Checking for common issues...")
    
    # Check file sizes
    if os.path.isfile("app.py"):
        size_mb = os.path.getsize("app.py") / (1024 * 1024)
        if size_mb < 1.0:
            print(f"  ✓ app.py size reasonable ({size_mb:.2f} MB)")
        else:
            print(f"  ⚠ app.py is large ({size_mb:.2f} MB)")
    
    print()
    print("=" * 60)
    
    if all_checks_passed:
        print("✓ All checks passed! Ready for deployment.")
        print()
        print("Next steps:")
        print("1. Review DEPLOYMENT.md for deployment instructions")
        print("2. Create a new Space at https://huggingface.co/new-space")
        print("3. Upload all files or use git push method")
        return 0
    else:
        print("✗ Some checks failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
