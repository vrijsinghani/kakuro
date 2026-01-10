# KDP Wraparound Cover Guide

## Your Book Specifications
- **Interior PDF:** `books/master-kakuro/output/interior.pdf`
- **Front Cover:** `books/master-kakuro/output/cover_front.png`
- **Page Count:** 326 pages
- **Trim Size:** 8.5" x 11" (Letter)
- **Paper Type:** White paper (assumed)

---

## Step 1: Calculate Spine Width

KDP uses this formula for **white paper**:
```
Spine Width = Page Count × 0.002252"
```

For your book:
```
326 × 0.002252 = 0.734" (approximately 0.73")
```

For **cream paper** (if you switch):
```
326 × 0.002500 = 0.815" (approximately 0.82")
```

---

## Step 2: Calculate Full Cover Dimensions

**Full wraparound cover = Back Cover + Spine + Front Cover + Bleed**

| Component | Width | Height |
|-----------|-------|--------|
| Front Cover | 8.5" | 11" |
| Back Cover | 8.5" | 11" |
| Spine | 0.73" | 11" |
| Bleed (each side) | 0.125" | 0.125" |

**Total Canvas Size:**
```
Width  = 0.125" + 8.5" + 0.73" + 8.5" + 0.125" = 17.98" ≈ 18"
Height = 0.125" + 11" + 0.125" = 11.25"
```

**At 300 DPI (print resolution):**
```
Width  = 18" × 300 = 5400 pixels
Height = 11.25" × 300 = 3375 pixels
```

---

## Step 3: Create the Wraparound Cover

### Option A: Use KDP Cover Creator (Easiest)
1. Go to KDP → Your Bookshelf → Select your book → Paperback Content
2. Click "Launch Cover Creator"
3. Upload `cover_front.png` as the front cover image
4. KDP will auto-generate the spine and let you customize the back cover
5. Download the final PDF

### Option B: Manual Creation (Full Control)

**Tools:** Canva, Adobe InDesign, Affinity Publisher, or GIMP

1. **Create a new canvas:** 18" × 11.25" at 300 DPI
2. **Mark the safe zones:**
   - Left 0.125": Bleed (will be trimmed)
   - 0.125" to 8.625": Back Cover
   - 8.625" to 9.355": Spine (0.73")
   - 9.355" to 17.855": Front Cover
   - 17.855" to 18": Bleed (will be trimmed)

3. **Place your front cover** (`cover_front.png`) on the RIGHT side (9.355" to 17.855")

4. **Design the spine:**
   - Text: "MASTER KAKURO" (rotated 90°, readable when book lies flat)
   - Optional: "Vol. 1" and author name
   - Keep text 0.0625" (1/16") away from spine edges

5. **Design the back cover:**
   - Book description / blurb
   - Barcode placeholder (KDP adds ISBN barcode automatically at bottom-right of back cover, leave 2" × 1.2" space)
   - Optional: Author photo, reviews, or additional marketing copy

6. **Export as PDF/X-1a:2001** (required by KDP) or high-res PNG

---

## Step 4: Verification Checklist

Before uploading to KDP:
- [ ] Total dimensions correct (18" × 11.25" or 5400 × 3375 px)
- [ ] All text 0.25" from trim edges (safety margin)
- [ ] Barcode area clear (2" × 1.2" bottom-right of back cover)
- [ ] Spine text is readable and centered
- [ ] Front cover matches the approved design
- [ ] File is RGB color mode (KDP converts to CMYK)
- [ ] Resolution is 300 DPI minimum

---

## Quick Reference: File Locations

| Asset | Path |
|-------|------|
| Interior PDF | `books/master-kakuro/output/interior.pdf` |
| Front Cover | `books/master-kakuro/output/cover_front.png` |
| This Guide | `books/master-kakuro/output/COVER_GUIDE.md` |

---

## KDP Cover Specifications Link
For the most up-to-date requirements:
https://kdp.amazon.com/en_US/help/topic/G201953020
