"""Export individual diagrams from Kakuro Chapter 1 HTML file."""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1200,1600")

# Create output directory
output_dir = "/home/ubuntu/kakuro_diagrams"
os.makedirs(output_dir, exist_ok=True)

# Initialize driver
driver = webdriver.Chrome(options=chrome_options)

try:
    # Load the HTML file
    driver.get("file:///home/ubuntu/kakuro_chapter1_visuals.html")
    time.sleep(2)

    # Find all diagram containers
    diagrams = driver.find_elements(By.CLASS_NAME, "diagram-container")
    print(f"Found {len(diagrams)} diagrams")

    # Export each diagram
    for i, diagram in enumerate(diagrams, 1):
        # Scroll to the diagram
        driver.execute_script("arguments[0].scrollIntoView(true);", diagram)
        time.sleep(0.5)

        # Take screenshot of the element
        screenshot_path = f"{output_dir}/diagram_{i}.png"
        diagram.screenshot(screenshot_path)
        print(f"Exported Diagram {i} to {screenshot_path}")

    print(f"\nSuccessfully exported {len(diagrams)} diagrams to {output_dir}/")

finally:
    driver.quit()
