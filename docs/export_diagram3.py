#!/usr/bin/env python3
"""Export Diagram 3 from Kakuro Chapter 2 visuals HTML to PNG."""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import os


def export_diagram3_to_png():
    """Export Diagram 3 from the HTML file to PNG."""
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1400,2000")
    chrome_options.add_argument("--hide-scrollbars")

    # Initialize the driver
    print("Initializing Chrome WebDriver...")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    )

    try:
        # Load the HTML file
        html_path = f"file:///home/ubuntu/kakuro_chapter2_visuals.html"
        print(f"Loading HTML file: {html_path}")
        driver.get(html_path)

        # Wait for page to load
        time.sleep(2)

        # Find all diagram containers
        diagram_containers = driver.find_elements(By.CLASS_NAME, "diagram-container")
        print(f"Found {len(diagram_containers)} diagram containers")

        # Get Diagram 3 (index 2, since it's the third diagram)
        if len(diagram_containers) >= 3:
            diagram3 = diagram_containers[2]

            # Scroll to the diagram
            driver.execute_script("arguments[0].scrollIntoView(true);", diagram3)
            time.sleep(1)

            # Create output directory if it doesn't exist
            output_dir = "/home/ubuntu/kakuro_chapter2_diagrams"
            os.makedirs(output_dir, exist_ok=True)

            # Take screenshot of Diagram 3
            output_path = os.path.join(output_dir, "diagram_3.png")
            print(f"Taking screenshot of Diagram 3...")
            diagram3.screenshot(output_path)

            # Get file size
            file_size = os.path.getsize(output_path)
            file_size_kb = file_size / 1024

            print(f"\n✅ SUCCESS!")
            print(f"Diagram 3 exported to: {output_path}")
            print(f"File size: {file_size_kb:.1f} KB")

            # Get image dimensions
            from PIL import Image

            img = Image.open(output_path)
            width, height = img.size
            print(f"Dimensions: {width} × {height} pixels")
            print(f'Physical size at 300 DPI: {width/300:.2f}" × {height/300:.2f}"')

        else:
            print("Error: Could not find Diagram 3 in the HTML file")

    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()

    finally:
        driver.quit()
        print("\nBrowser closed.")


if __name__ == "__main__":
    export_diagram3_to_png()
