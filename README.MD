# Text Extraction with PaddleOCR 📝🚀
This project extracts text from images using **PaddleOCR**, a powerful and efficient OCR engine. It supports multiple languages and works on various image formats.
**Accurate Text Detection** using PaddleOCR  
**Supports Multiple Languages**  
**Works with Different Image Formats** (JPG, PNG, etc.)  
**Custom Preprocessing for Improved OCR Performance**  

### 1️⃣ **Clone the Repository**
```bash
git clone https://github.com/iorliamterpase/paddleocr_text_extraction.git
cd text_extraction_paddleocr

##create and activate an environment
python -m venv venv
source venv/bin/activate  # For Mac/Linux
venv\Scripts\activate     # For Windows

##install dependencies
pip install -r requirements.txt

Note: Install PaddlePaddle based on your system (CPU/GPU).

For CPU: pip install paddlepaddle
For GPU: pip install paddlepaddle-gpu

##USAGE
run the script
main.py --image path/to/image.jpg

##TESTING
run the script
streamlit run app.py

##NOTE
make sure images are clear and readable




