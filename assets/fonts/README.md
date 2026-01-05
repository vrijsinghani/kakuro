# Fonts for Kakuro Puzzle Books

This directory contains free, commercially-licensed fonts for use in KDP puzzle book generation.

## Installed Fonts

### Roboto
- **License:** Apache License 2.0 (free for commercial use)
- **Use Case:** Primary font for puzzle numbers and grid text
- **Features:** Excellent readability, clean geometric design, great for numbers
- **Files:** `roboto/Roboto-*.ttf`

### Open Sans
- **License:** Apache License 2.0 (free for commercial use)
- **Use Case:** Instructions, headings, and body text
- **Features:** Humanist sans-serif, highly legible, professional appearance
- **Files:** `opensans/opensans-main/fonts/ttf/*.ttf`

### Noto Sans
- **License:** SIL Open Font License (free for commercial use)
- **Use Case:** Fallback font, alternative for numbers
- **Features:** Excellent Unicode coverage, clean and neutral design
- **Files:** `NotoSans-Regular.ttf`, `NotoSans-Bold.ttf`

## Font Recommendations for Kakuro

### For Puzzle Numbers (in cells)
- **Primary:** Roboto Regular or Roboto Medium
- **Size:** 10-14pt depending on grid size
- **Reason:** Clear, unambiguous digits (especially 1, 7, 9)

### For Clue Numbers (diagonal cells)
- **Primary:** Roboto Regular or Noto Sans Regular
- **Size:** 6-8pt
- **Reason:** Compact but readable at small sizes

### For Instructions
- **Primary:** Open Sans Regular
- **Size:** 10-12pt
- **Reason:** Comfortable reading for longer text

### For Headings
- **Primary:** Roboto Bold or Open Sans Bold
- **Size:** 14-18pt
- **Reason:** Clear hierarchy and professional look

## Adding New Fonts

To add new fonts:
1. Download the font files (.ttf or .otf)
2. Verify the license allows commercial use
3. Place in this directory or a subdirectory
4. Update this README with font details
5. Update `src/pdf_generation/font_manager.py` to register the font

## License Compliance

All fonts in this directory are licensed for commercial use. Always verify licenses before publishing.

- **Roboto:** https://github.com/google/roboto/blob/main/LICENSE
- **Open Sans:** https://github.com/googlefonts/opensans/blob/main/OFL.txt
- **Noto Sans:** https://github.com/notofonts/noto-fonts/blob/main/LICENSE

