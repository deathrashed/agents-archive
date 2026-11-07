#!/usr/bin/env python3
"""Validate README.md against the mandatory checklist."""

import argparse
import re
import sys


def check_readme(path):
    with open(path) as f:
        content = f.read()
    
    errors = []
    
    # 1. Hero block
    if not re.search(r'<div align="center">', content):
        errors.append("1. Missing hero block <div align='center'>")
    
    # 2. Badge palette
    if not re.search(r'Shields.io|shield.*badge', content):
        errors.append("2. No shields.io badges found")
    
    # 3. Tables
    if not re.search(r'\|[^\|]+\|', content):
        errors.append("3. No tables found")
    
    # 4. ASCII tree
    if not re.search(r'```text', content):
        errors.append("4. No ASCII directory tree found")
    
    # 5. Details cards
    if not re.search(r'<details>', content):
        errors.append("5. No collapsible details cards found")
    
    # 6. Section headers with icons
    headers = re.findall(r'^## .+$', content, re.MULTILINE)
    iconified = sum(1 for h in headers if re.search(r'<img src="http', h))
    if iconified < len(headers):
        errors.append("6. Some section headers lack Iconify SVG icons")
    
    return errors


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("readme")
    args = parser.parse_args()
    
    errors = check_readme(args.readme)
    if errors:
        print("Validation failed:")
        for e in errors:
            print(f"  ✗ {e}")
        sys.exit(1)
    else:
        print("✓ All mandatory checklist items passed")
        sys.exit(0)