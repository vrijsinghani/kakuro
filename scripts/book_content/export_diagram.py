#!/usr/bin/env python3
"""Export Diagram 2 from Kakuro Chapter 2 HTML file as PNG."""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os


def export_diagram_2():
    """Export Diagram 2 from the HTML file to PNG."""
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,3000")
    chrome_options.add_argument(
        "--force-device-scale-factor=2"
    )  # High DPI for better quality

    # Initialize the driver
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Load the HTML file
        html_path = f"file:///home/ubuntu/kakuro_chapter2_visuals.html"
        print(f"Loading HTML file: {html_path}")
        driver.get(html_path)

        # Wait for page to load
        time.sleep(2)

        # Find all diagram containers
        diagram_containers = driver.find_elements(By.CLASS_NAME, "diagram-container")

        if len(diagram_containers) < 2:
            print(
                f"Error: Expected at least 2 diagrams, found {len(diagram_containers)}"
            )
            return

        # Get Diagram 2 (index 1, since it's 0-indexed)
        diagram_2 = diagram_containers[1]

        # Scroll to the diagram
        driver.execute_script("arguments[0].scrollIntoView(true);", diagram_2)
        time.sleep(1)

        # Take screenshot of the specific element
        print("Taking screenshot of Diagram 2...")
        screenshot_path = "/home/ubuntu/kakuro_chapter2_diagrams/diagram_2.png"
        diagram_2.screenshot(screenshot_path)

        # Verify file was created
        if os.path.exists(screenshot_path):
            file_size = os.path.getsize(screenshot_path)
            print(f"✓ Screenshot saved successfully: {screenshot_path}")
            print(f"✓ File size: {file_size:,} bytes")
        else:
            print("✗ Error: Screenshot file was not created")

    except Exception as e:
        print(f"Error during export: {e}")
        import traceback

        traceback.print_exc()

    finally:
        driver.quit()
        print("Browser closed")


if __name__ == "__main__":
    export_diagram_2()
