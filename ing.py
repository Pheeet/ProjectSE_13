# Display the PDF pages as images so we can see the graph and identify the cut edges.
from pathlib import Path
from PIL import Image
import fitz  # PyMuPDF

pdf_path = "/mnt/data/Assign08Ch10_68.pdf"
doc = fitz.open(pdf_path)
images = []
for pageno in range(len(doc)):
    page = doc[pageno]
    pix = page.get_pixmap(dpi=200)
    img_path = f"/mnt/data/page_{pageno+1}.png"
    pix.save(img_path)
    images.append(img_path)

# Show image file paths so the UI will display them for you to view/download.
images[:10]  # return list of generated image paths


