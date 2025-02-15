import cv2
import argparse
import matplotlib.pyplot as plt
from paddleocr import PaddleOCR
import os

def process_image(image_path):
    image_path = os.path.join('.', 'images','10.jpg') 
    # Initialize PaddleOCR
    ocr = PaddleOCR(use_angle_cls=True, lang="en")

    # Run OCR
    results = ocr.ocr(image_path, cls=True)

    # Read image using OpenCV
    image = cv2.imread(image_path)

    # Extract and display text with bounding boxes
    extracted_text = []
    for result in results:
        for line in result:
            text = line[1][0]  # Extract text
            confidence = line[1][1]  # Confidence score
            extracted_text.append(text)
            print(f"Detected: {text} (Confidence: {confidence:.2f})")

            # Draw bounding box
            points = line[0]
            x_min, y_min = int(points[0][0]), int(points[0][1])
            x_max, y_max = int(points[2][0]), int(points[2][1])
            cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

            # Put text on image
            cv2.putText(image, text, (x_min, y_min - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2, cv2.LINE_AA)

    # Show image with detected words
    plt.figure(figsize=(10, 6))
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.axis("off")
    plt.show()

    return extracted_text

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OCR using PaddleOCR")
    parser.add_argument("--image", type=str, required=True, help="Path to the input image")
    args = parser.parse_args()

    # Run OCR
    text_output = process_image(args.image)
    print("\nExtracted Text:\n", "\n".join(text_output))
