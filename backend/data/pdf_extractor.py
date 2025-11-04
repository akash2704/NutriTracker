import pdfplumber 
import json
import re  # <-- 1. IMPORT THE REGEX LIBRARY
from pathlib import Path

# --- Robust Path (from our last lesson) ---
SCRIPT_DIR = Path(__file__).parent 
NIN_PDF_PATH = SCRIPT_DIR / "Dietry-guide-India.pdf"

class NINDataExtractor:

    def __init__(self,pdf_path):
        self.pdf_path=pdf_path
        # We can add our smoke test back in
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                print(f"✅ Successfully opened PDF. Total pages: {len(pdf.pages)}")
        except Exception as e:
            print(f"❌ Error opening PDF: {e}")

    def extract_cooked_food_data(self):
        print("Attempting to extract food data from Annexure 8...")
        
        # Correct 0-indexed pages for 117, 118, 119
        target_page_indices = [116, 117, 118] 
        all_cleaned_foods = []

        # This is our regex pattern.
        # r'(\d+)$' means:
        # ( ) = A "capture group" (save what you find)
        # \d+ = One or more digits
        # $   = At the *end* of the line
        calorie_pattern = re.compile(r'(\d+)$')

        with pdfplumber.open(self.pdf_path) as pdf:
            for page_index in target_page_indices:    
                current_page = pdf.pages[page_index]
                
                # --- NEW LOGIC: Get raw text ---
                text = current_page.extract_text()
                
                if not text:
                    print(f"⚠️ No text found on page {page_index + 1}. Skipping.")
                    continue
                
                print(f"--- Processing Page {page_index + 1} ---")
                
                # Split the entire page's text into a list of lines
                lines = text.split('\n')
                
                for line in lines:
                    # Skip category headers
                    if line.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.')):
                        continue

                    match = calorie_pattern.search(line)

                    if match:
                        calories = match.group(1)
                        description = line[:match.start()].strip()

                        # --- THIS IS THE FIX ---
                        # Check if the description contains any alphabetic characters
                        starts_with_number = bool(re.match(r'^\d', description))

                        # Update the final check to include has_letters
                        if description and not starts_with_number and "Preparation" not in description and "Annexure" not in description:
                        # --- END OF FIX ---
                            all_cleaned_foods.append({
                                "description": description,
                                "calories": calories
                            })
        
        return all_cleaned_foods

    def extract_rda_data(self):
        #TODO 
        pass

# --- 3. UNCOMMENT THIS BLOCK ---
if __name__=="__main__":
    print("🚀 Starting Data Extraction")
    extractor = NINDataExtractor(NIN_PDF_PATH)

    foods = extractor.extract_cooked_food_data()

    if foods:
        print(f"--- ✅ First 10 Cleaned Foods ---")
        for food in foods[:10]:
            print (food) # <-- Note: printing 'description' now
        print("---------------------------------")
        print(f"Successfully extracted and cleaned {len(foods)} foods.")