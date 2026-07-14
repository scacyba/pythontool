import fitz
from pptx import Presentation
from pptx.util import Inches
from pathlib import Path


#name = "大三島工場製造資料20260713追加_包装2班.pdf"
#pdf_path = rf"C:\Users\skacyba\Downloads\{name}"
#pptx_path = rf"{name}.pptx"

template = r"template.pptx"

folder = Path(r".")
prs = Presentation(template)
        
for pdf_path in folder.glob("*.pdf"):
    pptx_path = rf"{pdf_path}.pptx"
    doc = fitz.open(pdf_path)
    blank = prs.slide_layouts[6]

    for i, page in enumerate(doc):
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        img_path = f"page_{i+1}.png"
        pix.save(img_path)

        slide = prs.slides.add_slide(blank)
        slide.shapes.add_picture(img_path, 0, 0, width=prs.slide_width, height=prs.slide_height)

prs.save(pptx_path)

