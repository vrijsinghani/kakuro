#!/usr/bin/env python3
"""Export Diagrams 5 and 6 from Kakuro Chapter 2 HTML file as PNG images."""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os


def export_diagram(driver, diagram_index, output_path):
    """
    Export a specific diagram from the HTML file.

    Args:
        driver: Selenium WebDriver instance
        diagram_index: Index of the diagram container (0-based)
        output_path: Path to save the PNG file
    """
    # Find all diagram containers
    containers = driver.find_elements(By.CLASS_NAME, "diagram-container")

    if diagram_index >= len(containers):
        print(
            f"Error: Diagram index {diagram_index} out of range "
            f"(found {len(containers)} diagrams)"
        )
        return False

    diagram = containers[diagram_index]

    # Scroll to the diagram
    driver.execute_script("arguments[0].scrollIntoView(true);", diagram)
    time.sleep(0.5)

    # Take screenshot of the specific element
    diagram.screenshot(output_path)

    # Get file size
    file_size = os.path.getsize(output_path)
    print(f"✓ Exported diagram {diagram_index + 1} to {output_path}")
    print(f"  File size: {file_size / 1024:.1f} KB")

    return True


def main():
    """Export Diagrams 5 and 6 from the HTML file."""
    print("Starting export of Diagrams 5 and 6...")

    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1400,10000")

    # Initialize the driver
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Load the HTML file
        html_path = (
            f"file://{os.path.abspath('/home/ubuntu/kakuro_chapter2_visuals.html')}"
        )
        print(f"Loading: {html_path}")
        driver.get(html_path)

        # Wait for page to load
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "diagram-container")))
        time.sleep(2)  # Extra time for rendering

        # Create output directory if it doesn't exist
        output_dir = "/home/ubuntu/kakuro_chapter2_diagrams"
        os.makedirs(output_dir, exist_ok=True)

        # Export Diagram 5 (index 4, since it's the 5th diagram)
        print("\n--- Exporting Diagram 5 ---")
        diagram_5_path = os.path.join(output_dir, "diagram_5.png")
        export_diagram(driver, 4, diagram_5_path)

        # Export Diagram 6 (index 5, since it's the 6th diagram)
        print("\n--- Exporting Diagram 6 ---")
        diagram_6_path = os.path.join(output_dir, "diagram_6.png")
        export_diagram(driver, 5, diagram_6_path)

        print("\n✅ Export complete!")
        print(f"\nDiagrams saved to:")
        print(f"  • {diagram_5_path}")
        print(f"  • {diagram_6_path}")

    except Exception as e:
        print(f"❌ Error during export: {e}")
        import traceback

        traceback.print_exc()

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
