#!/usr/bin/env python3
"""Export full Diagram 2 from Kakuro Chapter 2 visuals using Selenium.

Script to export full Diagram 2 from the Kakuro Chapter 2 visuals HTML file
using Selenium WebDriver with Chrome - captures the entire scrollable content.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from PIL import Image
import time
import os

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--force-device-scale-factor=2")

# Initialize the Chrome driver
print("Initializing Chrome WebDriver...")
from webdriver_manager.chrome import ChromeDriverManager

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Load the HTML file
    html_path = "file:///home/ubuntu/kakuro_chapter2_visuals.html"
    print(f"Loading HTML file: {html_path}")
    driver.get(html_path)

    # Wait for page to load
    time.sleep(2)

    # Find Diagram 2 container
    print("Finding Diagram 2 container...")
    diagram_containers = driver.find_elements(By.CLASS_NAME, "diagram-container")

    if len(diagram_containers) < 2:
        raise Exception("Could not find Diagram 2 container")

    diagram2 = diagram_containers[1]  # Second diagram container

    # Get the full height of the diagram
    total_height = driver.execute_script("return arguments[0].scrollHeight", diagram2)
    viewport_height = driver.execute_script(
        "return arguments[0].clientHeight", diagram2
    )
    width = driver.execute_script("return arguments[0].scrollWidth", diagram2)

    print(f"Diagram dimensions: {width}px wide × {total_height}px tall")
    print(f"Viewport height: {viewport_height}px")

    # Scroll to the diagram and set window size to capture it fully
    driver.execute_script("arguments[0].scrollIntoView(true);", diagram2)
    time.sleep(1)

    # Increase window height to capture more content
    driver.set_window_size(1920, min(total_height + 200, 10000))
    time.sleep(1)

    # Create output directory if it doesn't exist
    output_dir = "/home/ubuntu/kakuro_chapter2_diagrams"
    os.makedirs(output_dir, exist_ok=True)

    # Take screenshot of the diagram
    output_path = os.path.join(output_dir, "diagram_2.png")
    print(f"Taking screenshot and saving to: {output_path}")

    # Get the element screenshot with full height
    diagram2.screenshot(output_path)

    print(f"✓ Successfully exported Diagram 2 to {output_path}")

    # Verify the file was created
    if os.path.exists(output_path):
        file_size = os.path.getsize(output_path)
        print(f"  File size: {file_size / 1024:.1f} KB")

        # Get image dimensions
        img = Image.open(output_path)
        print(f"  Image dimensions: {img.width} × {img.height} pixels")
        print(f"  Image format: {img.format}")

except Exception as e:
    print(f"✗ Error: {str(e)}")
    import traceback

    traceback.print_exc()

finally:
    # Close the browser
    print("Closing browser...")
    driver.quit()
    print("Done!")
