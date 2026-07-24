#!/usr/bin/env python3
import json
import os
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: generate_layout_boilerplate.py <template_name>")
        sys.exit(1)
        
    template_name = sys.argv[1]
    assets_dir = os.path.join(os.path.dirname(__file__), '../assets')
    
    with open(os.path.join(assets_dir, 'layout_templates.json'), 'r') as f:
        templates = json.load(f)
        
    if template_name not in templates:
        print(f"Error: Template '{template_name}' not found.")
        sys.exit(1)
        
    print(templates[template_name]['code'])

if __name__ == "__main__":
    main()
