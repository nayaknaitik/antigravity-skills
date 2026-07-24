#!/usr/bin/env python3
import sys
import argparse

def get_luminance(hex_color):
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    
    def adjust(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
        
    return 0.2126 * adjust(r) + 0.7152 * adjust(g) + 0.0722 * adjust(b)

def get_contrast_ratio(c1, c2):
    lum1 = get_luminance(c1)
    lum2 = get_luminance(c2)
    brightest = max(lum1, lum2)
    darkest = min(lum1, lum2)
    return (brightest + 0.05) / (darkest + 0.05)

def main():
    parser = argparse.ArgumentParser(description="Validate WCAG Contrast Ratio")
    parser.add_argument("fg", help="Foreground hex color (e.g., #FFFFFF)")
    parser.add_argument("bg", help="Background hex color (e.g., #0F172A)")
    args = parser.parse_args()

    ratio = get_contrast_ratio(args.fg, args.bg)
    print(f"Contrast Ratio: {ratio:.2f}:1")
    
    if ratio >= 4.5:
        print("Status: PASS (AA compliant)")
    else:
        print("Status: FAIL (Below 4.5:1 ratio)")
        sys.exit(1)

if __name__ == "__main__":
    main()
