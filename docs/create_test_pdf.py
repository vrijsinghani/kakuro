#!/usr/bin/env python3
"""Create test PDF showing Diagram 2 layout options for KDP printing."""

from reportlab.lib.pagesizes import letter, inch
from reportlab.pdfgen import canvas
from PIL import Image
import os

# File paths
diagram_path = "/home/ubuntu/kakuro_chapter2_diagrams/diagram_2.png"
output_pdf = "/home/ubuntu/diagram_2_layout_test.pdf"

# Get diagram dimensions
img = Image.open(diagram_path)
diagram_width_px, diagram_height_px = img.size
dpi = 300

# Page setup for 8.5" x 11" (letter size)
page_width, page_height = letter  # 8.5" x 11" in points (612 x 792)
margin_left = 0.75 * inch
margin_right = 0.75 * inch
margin_top = 0.5 * inch
margin_bottom = 0.5 * inch

printable_width = page_width - margin_left - margin_right
printable_height = page_height - margin_top - margin_bottom

# Create PDF
c = canvas.Canvas(output_pdf, pagesize=letter)

# ===== PAGE 1: TITLE PAGE WITH ANALYSIS =====
c.setFont("Helvetica-Bold", 18)
c.drawCentredString(page_width / 2, page_height - 1 * inch, "Diagram 2 Layout Analysis")

c.setFont("Helvetica-Bold", 14)
c.drawCentredString(
    page_width / 2, page_height - 1.5 * inch, "Chapter 2: The Elimination Method"
)

# Analysis box
y = page_height - 2.5 * inch
c.setFont("Helvetica-Bold", 12)
c.drawString(margin_left, y, "📐 DIAGRAM SPECIFICATIONS:")
y -= 0.3 * inch

c.setFont("Helvetica", 11)
c.drawString(
    margin_left + 0.3 * inch,
    y,
    f"• Dimensions: {diagram_width_px} × {diagram_height_px} pixels",
)
y -= 0.25 * inch
c.drawString(margin_left + 0.3 * inch, y, f'• Physical size at 300 DPI: 4.00" × 16.43"')
y -= 0.25 * inch
c.drawString(margin_left + 0.3 * inch, y, f'• Target page size: 8.5" × 11"')
y -= 0.25 * inch
c.drawString(margin_left + 0.3 * inch, y, f'• Printable area: 7.00" × 10.00"')

y -= 0.5 * inch
c.setFont("Helvetica-Bold", 12)
c.drawString(margin_left, y, "⚠️  FINDING:")
y -= 0.3 * inch

c.setFont("Helvetica", 11)
c.setFillColorRGB(0.8, 0, 0)
c.drawString(
    margin_left + 0.3 * inch,
    y,
    'Diagram is 16.43" tall - TOO TALL to fit on one 11" page!',
)
c.setFillColorRGB(0, 0, 0)

y -= 0.5 * inch
c.setFont("Helvetica-Bold", 12)
c.drawString(margin_left, y, "📊 LAYOUT OPTIONS SHOWN IN THIS PDF:")
y -= 0.3 * inch

c.setFont("Helvetica", 11)
c.drawString(
    margin_left + 0.3 * inch,
    y,
    "• Option 1 (Pages 2-3): Split across 2 pages ✅ RECOMMENDED",
)
y -= 0.25 * inch
c.drawString(
    margin_left + 0.3 * inch,
    y,
    "• Option 2 (Page 4): Scaled to fit 1 page ❌ NOT recommended",
)

y -= 0.5 * inch
c.setFont("Helvetica-Bold", 12)
c.setFillColorRGB(0, 0.5, 0)
c.drawString(margin_left, y, "✅ RECOMMENDATION:")
c.setFillColorRGB(0, 0, 0)
y -= 0.3 * inch

c.setFont("Helvetica", 11)
c.drawString(
    margin_left + 0.3 * inch, y, "Use Option 1 - Split across 2 pages to maintain"
)
y -= 0.25 * inch
c.drawString(
    margin_left + 0.3 * inch, y, "large print readability for 50-70 age demographic."
)

y -= 0.8 * inch
c.setFont("Helvetica-Oblique", 10)
c.setFillColorRGB(0.3, 0.3, 0.3)
c.drawString(margin_left, y, "Turn the page to see Option 1 (2-page split) →")
c.setFillColorRGB(0, 0, 0)

c.showPage()

# ===== OPTION 1: SPLIT ACROSS 2 PAGES =====

# Calculate split point (approximately in the middle, but at a logical break)
# Split after Grid 2 (roughly at pixel 2000 out of 4930)
split_height_px = 2465  # Split roughly in half

# PAGE 2: First half
c.setFont("Helvetica-Bold", 14)
c.drawString(
    margin_left, page_height - 0.5 * inch, "Option 1: Two-Page Layout (Page 1 of 2)"
)

c.setFont("Helvetica", 10)
c.drawString(
    margin_left,
    page_height - 0.7 * inch,
    "Grids 1-2: Introduction and first steps of elimination method",
)

# Draw first half of diagram at full width
diagram_scale = printable_width / (diagram_width_px / dpi)
first_half_height = (split_height_px / dpi) * diagram_scale

# Crop and draw first half
img_first = img.crop((0, 0, diagram_width_px, split_height_px))
temp_first = "/tmp/diagram_first_half.png"
img_first.save(temp_first)

c.drawImage(
    temp_first,
    margin_left,
    margin_bottom,
    width=printable_width,
    height=first_half_height,
    preserveAspectRatio=True,
)

# Add continuation note
c.setFont("Helvetica-Oblique", 10)
c.setFillColorRGB(0, 0, 0.7)
c.drawCentredString(
    page_width / 2, margin_bottom - 0.3 * inch, "Continued on next page →"
)
c.setFillColorRGB(0, 0, 0)

c.showPage()

# PAGE 3: Second half
c.setFont("Helvetica-Bold", 14)
c.drawString(
    margin_left, page_height - 0.5 * inch, "Option 1: Two-Page Layout (Page 2 of 2)"
)

c.setFont("Helvetica", 10)
c.drawString(
    margin_left,
    page_height - 0.7 * inch,
    "Grids 3-5: Completing the elimination method and solution",
)

# Draw second half of diagram
second_half_height_px = diagram_height_px - split_height_px
second_half_height = (second_half_height_px / dpi) * diagram_scale

img_second = img.crop((0, split_height_px, diagram_width_px, diagram_height_px))
temp_second = "/tmp/diagram_second_half.png"
img_second.save(temp_second)

# Position second half
y_position = page_height - margin_top - 0.9 * inch - second_half_height

c.drawImage(
    temp_second,
    margin_left,
    y_position,
    width=printable_width,
    height=second_half_height,
    preserveAspectRatio=True,
)

c.showPage()

# ===== OPTION 2: SCALED TO FIT ON 1 PAGE =====

c.setFont("Helvetica-Bold", 14)
c.drawString(
    margin_left, page_height - 0.5 * inch, "Option 2: One-Page Layout (Scaled Down)"
)

c.setFont("Helvetica", 10)
c.setFillColorRGB(0.8, 0, 0)
c.drawString(
    margin_left,
    page_height - 0.7 * inch,
    "⚠️ NOT RECOMMENDED: Text becomes too small for 50-70 age group",
)
c.setFillColorRGB(0, 0, 0)

# Scale to fit available height
scale_factor = printable_height / (diagram_height_px / dpi)
scaled_width = (diagram_width_px / dpi) * scale_factor
scaled_height = printable_height

# Center horizontally if scaled width is less than printable width
x_position = margin_left + (printable_width - scaled_width) / 2

c.drawImage(
    diagram_path,
    x_position,
    margin_bottom,
    width=scaled_width,
    height=scaled_height,
    preserveAspectRatio=True,
)

# Add warning note
c.setFont("Helvetica-Bold", 10)
c.setFillColorRGB(0.8, 0, 0)
c.drawCentredString(
    page_width / 2,
    margin_bottom - 0.3 * inch,
    f"Scaled to {scale_factor*100:.1f}% - Too small for target audience!",
)
c.setFillColorRGB(0, 0, 0)

c.showPage()

# ===== FINAL RECOMMENDATION PAGE =====

c.setFont("Helvetica-Bold", 18)
c.drawCentredString(page_width / 2, page_height - 1 * inch, "Final Recommendation")

y = page_height - 2 * inch

c.setFont("Helvetica-Bold", 14)
c.setFillColorRGB(0, 0.5, 0)
c.drawString(margin_left, y, "✅ USE OPTION 1: Two-Page Layout")
c.setFillColorRGB(0, 0, 0)
y -= 0.5 * inch

c.setFont("Helvetica-Bold", 12)
c.drawString(margin_left, y, "Benefits:")
y -= 0.3 * inch

c.setFont("Helvetica", 11)
benefits = [
    "• Maintains full size and readability for 50-70 age group",
    "• Each grid is clear and easy to see",
    "• Professional appearance with logical page break",
    "• No compromise on large print format",
    "• Natural break between steps 2 and 3",
]

for benefit in benefits:
    c.drawString(margin_left + 0.3 * inch, y, benefit)
    y -= 0.25 * inch

y -= 0.3 * inch
c.setFont("Helvetica-Bold", 12)
c.drawString(margin_left, y, "Implementation:")
y -= 0.3 * inch

c.setFont("Helvetica", 11)
steps = [
    "1. Split diagram after Grid 2 (first page shows Grids 1-2)",
    "2. Add 'Continued on next page →' at bottom of first page",
    "3. Second page shows Grids 3-5 with solution",
    "4. Optionally add '← Continued from previous page' at top",
    "5. Keep consistent formatting and margins on both pages",
]

for step in steps:
    c.drawString(margin_left + 0.3 * inch, y, step)
    y -= 0.25 * inch

y -= 0.5 * inch
c.setFont("Helvetica-Bold", 12)
c.setFillColorRGB(0.8, 0, 0)
c.drawString(margin_left, y, "❌ Avoid Option 2:")
c.setFillColorRGB(0, 0, 0)
y -= 0.3 * inch

c.setFont("Helvetica", 11)
c.drawString(
    margin_left + 0.3 * inch,
    y,
    "Scaling down defeats the purpose of a large print book",
)
y -= 0.25 * inch
c.drawString(margin_left + 0.3 * inch, y, "and would frustrate your target audience.")

c.save()

print(f"✅ Test PDF created: {output_pdf}")
print(f"   File size: {os.path.getsize(output_pdf) / 1024:.1f} KB")
print()
print("📄 The PDF contains:")
print("   • Page 1: Analysis and specifications")
print("   • Pages 2-3: Option 1 (Two-page split) ✅ RECOMMENDED")
print("   • Page 4: Option 2 (Scaled to one page) ❌ Not recommended")
print("   • Page 5: Final recommendation and implementation guide")
