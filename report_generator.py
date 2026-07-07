from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
import datetime

def generate_criminal_report(criminal_data, image_path, save_path="criminal_report.pdf"):

    c = canvas.Canvas(save_path, pagesize=A4)
    width, height = A4

    # Title 
    c.setFont("Helvetica-Bold", 22)
    c.drawString(150, height - 80, "CRIMINAL DETECTION REPORT")

    # Basic Info Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 140, "Criminal Details")

    # Criminal information
    c.setFont("Helvetica", 13)

    y = height - 170
    for key, value in criminal_data.items():
        c.drawString(50, y, f"{key}: {value}")
        y -= 20

    # Add detected timestamp
    detect_time = datetime.datetime.now().strftime("%d-%m-%Y  %H:%M:%S")
    c.drawString(50, y - 20, f"Detected Time: {detect_time}")

    # Add criminal photo
    try:
        c.drawImage(ImageReader(image_path), 350, height - 320, width=180, height=220)
    except:
        c.drawString(350, height - 320, "Image Load Failed")

    c.save()
    print("PDF Report Generated:", save_path)
