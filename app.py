import streamlit as st
from paddleocr import PaddleOCR
import os
from PIL import Image
import re

# Initialize PaddleOCR
ocr_model = PaddleOCR(use_angle_cls=True, lang="en")

# Function to process the image
def extract_text_from_image(image):
    # Save the uploaded image to a temporary location
    img_path = "temp_image.jpg"
    image.save(img_path)

    # Process the image with PaddleOCR
    results = ocr_model.ocr(img_path, cls=True)

    # Extract text from OCR results
    extracted_text = []
    for result in results:
        if result:  # Ensure it's not empty
            for line in result:
                if isinstance(line, list) and len(line) > 1:
                    extracted_text.append(line[1][0])
    
    # Remove the temporary image after processing
    os.remove(img_path)

    return extracted_text

# Streamlit app UI
def main():
    st.title("PaddleOCR Text Extraction App")
    st.markdown("Upload an image to extract text from it using PaddleOCR.")

    # Image upload section
    uploaded_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)

        # Extract text from the image
        st.write("Extracting text...")
        extracted_text = extract_text_from_image(image)

        # Display extracted text
        if extracted_text:
            st.subheader("Extracted Text:")
            st.write("\n".join(extracted_text))
        else:
            st.write("No text found in the image.")

            st.markdown("### 🛒 ")


# Add custom background color
st.markdown(
    """
    <style>
    .stApp {
        background-color: green;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: red;
        padding: 10px 20px;
        font-size: 16px;
        border-radius: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)



def clean_extracted_text(extracted_text):
    # Remove unnecessary characters (such as asterisks)
    cleaned_text = extracted_text.replace('*', '').strip()
    
    # Split text into lines based on newlines or other delimiters
    lines = cleaned_text.split("\n")
    
    # Create structured data for items
    items = []
    totals = {}
    store_info = {}
    date_info = {}

    # Process the lines and categorize them
    for line in lines:
        # Identifying store information (e.g., name, email, VAT)
        if "SPARC" in line or "email" in line or "VAT" in line:
            store_info['Store Info'] = line.strip()
        
        # Extract item details (Product name, Quantity, Price)
        elif re.match(r"^\D+(\d+\.\d{2})", line):  # Looks for price format
            item_details = re.split(r'(\d+\.\d{2})', line)
            if len(item_details) > 1:
                item = {
                    'item': item_details[0].strip(),
                    'price': item_details[1].strip()
                }
                items.append(item)
        
        # Extract total and tax-related information
        elif 'TOTAL FOR' in line or 'TENDERED' in line:
            totals['Total'] = line.strip()
        
        # Extract Date and Time
        elif re.match(r"\d{2}\.\d{2}\.\d{2}", line):  # Looks like a date
            date_info['Date'] = line.strip()

    # Organize structured output
    structured_output = {
        'Store Info': store_info,
        'Items': items,
        'Totals': totals,
        'Date Info': date_info
    }
    
    return structured_output

# Extracted text (as provided)
extracted_text = """SPARC Te1036-4481240 email :bergspar@telkomsa.net VAT No4450102696 NLA REG NOKZN 032577 17.99 A LAZENBY WORCESTER SAUCE 125ML 80GR 16.99 A MILKY BAR CHOC 500GR 33.99A SMOKED VIENNAS 400G 82.99A PEALED PEACHES 1KG 44.99* MEDITERRANEAN MIX 375ML 14.99 * SPAR COOKING OIL 1'S 12.99* F/L ENGLISH CUCUMB 85GR 20.99A NESTLE AERO 80GR 16.99 A CADBURY DAIRY MI TUB 24.99* GRAPES MIXED TUB 500GR 11.99* TASTIC RICE 270GR 27.99 A BLACK CAT SMOOTH CARRIER BAG 24L 1'S 0.75 A BANANAS LOOSE 17KG 15.99R /kg 9.53* 0.596kg@ TOTAL FOR 14 ITEMS 338.16 TENDERED Nedbank 338.16 TAX INVOICE VAT rate excl. TAX incl. 0.00% 119.48 0.00 119.48* 15.00% 190.16 28.52 218.68 A SLIP TILL /CASHIER DATE TIME 3780 005 101 23.02.21 16:17 CASHIER NAME:SWAZI Please Retain Slip Thank You For Shopping With Us) Follow us on Facebook: Spar Bergville"""

# Clean the extracted text
structured_data = clean_extracted_text(extracted_text)

# Display the cleaned and structured data
for section, content in structured_data.items():
    print(f"{section}:")
    if isinstance(content, list):
        for item in content:
            print(f"  - Item: {item['item']} | Price: {item['price']}")
    else:
        print(f"  {content}")
    print()


if __name__ == "__main__":
    main()


