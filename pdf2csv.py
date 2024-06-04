import streamlit as st
import camelot
import pandas as pd
import os

# Set the app title
st.set_page_config(page_title="PDF Table Extractor")

# Add a title
st.title("PDF Table Extractor")

# File uploader
pdf_files = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)

# Process the PDF files if any are uploaded
if pdf_files:
    # Allow the user to select the output format
    output_format = st.selectbox("Select output format", ["CSV", "Excel"])

    # Create a directory to store the extracted tables
    if not os.path.exists("extracted_tables"):
        os.makedirs("extracted_tables")

    # Loop through each uploaded file
    for pdf_file in pdf_files:
        # Get the file name
        file_name = pdf_file.name

        # Display the file name
        st.write(f"Processing file: {file_name}")

        # Save the uploaded PDF to a temporary file
        with open(file_name, "wb") as f:
            f.write(pdf_file.read())

        # Extract tables from the PDF
        tables = camelot.read_pdf(file_name, pages='all')

        # Display the extracted tables
        st.write("Extracted Tables:")
        for i, table in enumerate(tables):
            st.write(f"Table {i+1}:")
            st.write(table.df)

        # Save the extracted tables
        if output_format == "CSV":
            for i, table in enumerate(tables):
                table.to_csv(f"extracted_tables/{file_name.split('.')[0]}_table_{i+1}.csv", index=False)
            st.success(f"Tables from {file_name} saved as CSV files.")
        else:
            for i, table in enumerate(tables):
                table.to_excel(f"extracted_tables/{file_name.split('.')[0]}_table_{i+1}.xlsx", index=False)
            st.success(f"Tables from {file_name} saved as Excel files.")

    if output_format == "CSV":
        st.success("All tables saved as CSV files in the 'extracted_tables' directory.")
    else:
        st.success("All tables saved as Excel files in the 'extracted_tables' directory.")

# Add some information about the app
st.write("This app uses the `camelot` library to extract tables from PDF files.")
st.write("You can upload one or more PDF files, and the app will extract tables from them and display them.")
st.write("You can then choose to save the extracted tables as CSV or Excel files.")
