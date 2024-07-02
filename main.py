import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from PIL import Image
from datetime import datetime
import zipfile
import os

# Rutas de las imágenes comunes
ruta_imagen_comun = "escudo.jpg"
ruta_firma_comun = "firma.jpg"
ruta_qr_comun = "qr.jpg"

def generate_pdf(data, output_path):
    # Set up the canvas
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    # Image dimensions
    img_width, img_height = 363, 241

    # Center the image at the top
    img_x = (width - img_width) / 2
    img_y = height - img_height - 50  # 50 units from the top
    c.drawImage(ruta_imagen_comun, img_x, img_y, width=img_width, height=img_height)

    # Set up text
    text_y = img_y - 100  # Space between image and text

    # Format the date
    formatted_date = datetime.strptime(data['date'], "%Y-%m-%d").strftime("México, Ciudad de México, a %d de %B del %Y")

    # Draw text from CSV parameters
    c.setFont("Helvetica", 12)
    text = f"""
    {formatted_date}
    Nombre: {data['name']}
    {data['texto_parametrizable']}
    Email: {data['email']}
    """
    lines = text.strip().split("\n")
    for line in lines:
        text_width = c.stringWidth(line, "Helvetica", 12)
        text_x = (width - text_width) / 2
        c.drawString(text_x, text_y, line.strip())
        text_y -= 20  # Line height

    # Add space for signature
    signature_y = text_y - 70  # 70 units of space for signature and name

    # Draw signature image
    firma_img = Image.open(ruta_firma_comun)
    firma_width, firma_height = firma_img.size
    firma_x = (width - firma_width) / 2
    firma_y = signature_y - firma_height - inch / 2  # 1.5 cm above the bottom
    c.drawImage(ruta_firma_comun, firma_x, firma_y, width=firma_width, height=firma_height)

    # Draw QR code image
    qr_img = Image.open(ruta_qr_comun)
    qr_width, qr_height = qr_img.size
    qr_x = (width - qr_width) / 2
    qr_y = firma_y - qr_height - inch / 2  # 1.5 cm above the signature
    c.drawImage(ruta_qr_comun, qr_x, qr_y, width=qr_width, height=qr_height)

    # Add name below signature
    c.drawString((width - c.stringWidth(data['firma_name'], "Helvetica", 12)) / 2, qr_y + 90, data['firma_name'])

    # Save the PDF
    c.save()

def read_excel_data(excel_file):
    data_list = []
    df = pd.read_excel(excel_file)

    for _, row in df.iterrows():
        data = {
            'name': row['Nombre'],
            'date': row['Fecha'],
            'email': row['Email'],
            'texto_parametrizable': row['TextoParametrizable'],
            'firma_name': row['NombreFirma']
        }
        data_list.append(data)

    return data_list

def create_zip(files, zip_name):
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        for file in files:
            zipf.write(file, os.path.basename(file))

def main():
    st.title("Generador de PDFs")
    
    uploaded_file = st.file_uploader("Carga tu archivo Excel", type=["xlsx"])
    
    if uploaded_file is not None:
        data_list = read_excel_data(uploaded_file)

        pdf_files = []
        for data in data_list:
            output_path = f"{data['name']}.pdf"
            generate_pdf(data, output_path)
            pdf_files.append(output_path)

        zip_name = "pdfs.zip"
        create_zip(pdf_files, zip_name)

        with open(zip_name, "rb") as zip_file:
            st.download_button(
                label="Descargar archivos ZIP",
                data=zip_file,
                file_name="pdfs.zip",
                mime="application/zip"
            )
        
        # Clean up generated files
        for file in pdf_files:
            os.remove(file)
        os.remove(zip_name)

if __name__ == "__main__":
    main()
