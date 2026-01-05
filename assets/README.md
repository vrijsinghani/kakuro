# Assets

This directory contains all static assets used in book generation.

## Directory Structure

### `fonts/`
Font files for PDF generation.

**Required fonts:**
- Professional, print-friendly fonts
- Must be commercially licensed or open-source
- Embedded in PDFs for consistent rendering

**Recommended fonts:**
- **Liberation Sans** - Open-source Arial alternative
- **Liberation Serif** - Open-source Times New Roman alternative
- **DejaVu Sans** - Excellent Unicode coverage
- **Roboto** - Modern, clean sans-serif

**Font requirements:**
- TrueType (.ttf) or OpenType (.otf) format
- Include regular, bold, italic, and bold-italic variants
- License must allow commercial use and embedding

**Sources:**
- Google Fonts: https://fonts.google.com
- Font Squirrel: https://www.fontsquirrel.com
- Liberation Fonts: https://github.com/liberationfonts/liberation-fonts

### `images/`
Image assets for books and marketing.

#### `images/logos/`
Brand logos and publisher marks.
- Publisher logo (if applicable)
- Series branding elements
- Author/brand watermarks

**Formats:** PNG with transparency, SVG for scalability

#### `images/graphics/`
Decorative elements and illustrations.
- Border designs
- Section dividers
- Instructional diagrams
- Example puzzle illustrations

**Requirements:**
- 300 DPI minimum for print
- CMYK color mode preferred
- PNG or TIFF format

### `templates/`
Reusable templates for book components.

#### `templates/covers/`
Cover design templates.
- Front cover layouts
- Back cover layouts
- Spine designs
- Full wrap templates (front + spine + back)

**File formats:**
- PSD (Photoshop) - editable source files
- PDF - print-ready exports
- PNG - preview images

**KDP cover dimensions:**
Calculated as: `(bleed + trim width + bleed) × (bleed + trim height + bleed) + spine width`

Example for 8.5" × 11", 200 pages:
- Trim: 8.5" × 11"
- Bleed: 0.125" on all sides
- Spine: ~0.44" (depends on page count and paper type)
- Total cover: 17.375" × 11.25"

#### `templates/interiors/`
Interior page templates.
- Puzzle page layouts
- Solution page layouts
- Instruction page layouts
- Title page templates
- Copyright page templates

**Specifications:**
- Match book trim size
- Include bleed if using full-page backgrounds
- Safe zone: 0.375" from edges for text

#### `templates/instructions/`
"How to Play" instruction templates.
- Beginner-friendly explanations
- Visual examples
- Step-by-step solving guides
- Rule summaries

**Formats:**
- Markdown for easy editing
- PDF for final layout
- Images for diagrams

## Asset Management

### Naming Conventions
- Use lowercase with underscores: `cover_template_beginner.psd`
- Include size/variant in name: `logo_publisher_300dpi.png`
- Version control: `cover_v1.psd`, `cover_v2.psd`

### File Organization
- Keep source files (PSD, AI, SVG) separate from exports
- Maintain both RGB (screen) and CMYK (print) versions
- Archive old versions in `archive/` subdirectories

### Quality Standards
- **Images:** 300 DPI minimum, CMYK for print
- **Fonts:** Properly licensed, all variants included
- **Templates:** Documented with usage instructions
- **Colors:** Use CMYK values, avoid RGB-only colors

### License Compliance
- Document license for each asset in `LICENSES.txt`
- Only use assets with commercial use rights
- Attribute sources where required
- Keep license files with downloaded fonts

## Adding New Assets

1. **Verify license** - Ensure commercial use is allowed
2. **Optimize for print** - 300 DPI, CMYK, proper format
3. **Document source** - Add to `LICENSES.txt` or `SOURCES.md`
4. **Organize properly** - Place in correct subdirectory
5. **Update README** - Document new asset types if needed

## Resources

### Free Commercial Fonts
- Google Fonts: https://fonts.google.com
- Font Squirrel: https://www.fontsquirrel.com
- The League of Moveable Type: https://www.theleagueofmoveabletype.com

### Free Stock Images
- Unsplash: https://unsplash.com (free for commercial use)
- Pexels: https://www.pexels.com (free for commercial use)
- Pixabay: https://pixabay.com (free for commercial use)

### Design Tools
- GIMP (free): https://www.gimp.org
- Inkscape (free): https://inkscape.org
- Canva (freemium): https://www.canva.com
- Adobe Creative Cloud (paid): Photoshop, Illustrator, InDesign

