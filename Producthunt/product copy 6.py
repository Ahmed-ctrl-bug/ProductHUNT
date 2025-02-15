import os
from playwright.sync_api import sync_playwright

def main():
    # Print the current working directory so you know where the output file is saved.
    cwd = os.getcwd()
    print("Current working directory:", cwd)
    
    output_lines = []  # List to collect output lines
    
    with sync_playwright() as p:
        # Launch the browser (set headless=False for debugging)
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Navigate to Product Hunt
        page.goto("https://www.producthunt.com/")

        # Wait for the sections to load (adjust timeout as necessary)
        page.wait_for_selector("xpath=/html/body/div[1]/div[3]/main/div/div[1]/section", timeout=60000)
        
        # Take a full-page screenshot for debugging purposes (optional)
        page.screenshot(path="debug_full_page.png", full_page=True)
        print("Debug screenshot saved as debug_full_page.png")
        output_lines.append("Debug screenshot saved as debug_full_page.png")
        
        # Get all section elements following the XPath pattern
        sections = page.locator("xpath=/html/body/div[1]/div[3]/main/div/div[1]/section")
        sections_count = sections.count()
        info_line = f"Found {sections_count} sections."
        print(info_line)
        output_lines.append(info_line)
        
        # Iterate over each section
        for i in range(sections_count):
            section_xpath = f"/html/body/div[1]/div[3]/main/div/div[1]/section[{i+1}]/div/a"
            a_elements = page.locator(f"xpath={section_xpath}")
            a_count = a_elements.count()
            line = f"Section {i+1} has {a_count} link(s)."
            print(line)
            output_lines.append(line)
            
            # Iterate over each <a> element in the current section
            for j in range(a_count):
                try:
                    text = a_elements.nth(j).text_content(timeout=10000)
                    line = f"Section {i+1}, Link {j+1}: {text.strip()}"
                    print(line)
                    output_lines.append(line)
                except Exception as e:
                    error_line = f"Error retrieving text for Section {i+1}, Link {j+1}: {e}"
                    print(error_line)
                    output_lines.append(error_line)
        
        browser.close()

    # Save the collected output lines to "output.txt" in the current working directory.
    output_file = os.path.join(cwd, "output.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        for line in output_lines:
            f.write(line + "\n")
    print(f"Output saved to {output_file}")

if __name__ == "__main__":
    main()