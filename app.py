import streamlit as st
import pdfplumber
import pytesseract
from PIL import Image
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="PDF Table Extractor")

st.markdown("""
    ## Extract Tables from PDF
    Upload a PDF to extract tables and display them as a DataFrame.
    Optionally enable OCR for scanned documents.
""")

ocr_enabled = st.checkbox('Enable OCR for scanned documents')
pdf_file = st.file_uploader("Load your PDF", type=['pdf'])

hide = """
<style>
footer {
    visibility: hidden;
    position: relative;
}
.viewerBadge_container__1QSob {
    visibility: hidden;
}
#MainMenu {
    visibility: hidden;
}
</style>
"""
st.markdown(hide, unsafe_allow_html=True)

def ocr_image(image):
    return pytesseract.image_to_string(image)

def extract_text_from_page(page):
    if page.extract_text():
        return page.extract_text()
    else:
        img = page.to_image()
        return ocr_image(img.original)

if pdf_file:
    all_tables = []

    with pdfplumber.open(pdf_file) as pdf:
        for page_num, page in enumerate(pdf.pages):
            if ocr_enabled:
                # For OCR-enabled documents, extract text using OCR if needed
                page_text = extract_text_from_page(page)
                # Split page_text into lines
                lines = page_text.split('\n')
                # Assuming table extraction on raw text here for simplicity
                # If the text contains structured data, you need to parse it accordingly
                data = [line.split() for line in lines]
                if data:
                    df = pd.DataFrame(data)
                    df['Page'] = page_num + 1
                    all_tables.append(df)
            else:
                tables = page.extract_tables()
                for table in tables:
                    df = pd.DataFrame(table[1:], columns=table[0])
                    df['Page'] = page_num + 1
                    all_tables.append(df)
    
    if all_tables:
        combined_df = pd.concat(all_tables, ignore_index=True)
        st.write(combined_df)
        
        csv = combined_df.to_csv(index=False)
        st.download_button(
            label="Download DataFrame as CSV",
            data=csv,
            file_name="pdf_table_data.csv",
            mime="text/csv"
        )
    else:
        st.info("No tables found in the PDF.")
