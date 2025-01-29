import streamlit as st
from ingestion.ingestion import process_pdfs_and_create_vectorstore_with_ai
import os
import tempfile
from frontend.ui.factory import UIFactory
from frontend.ui.base import UIRenderer

def render_document_uploader(ui: UIRenderer = None):
    """Render the document uploader section in the right sidebar."""
    ui = ui or UIFactory.create()
    
    st.markdown("### Document Upload")
    
    # File uploader for PDFs
    uploaded_files = ui.file_uploader(
        "Upload CV documents",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
        help="You can upload one or multiple PDF, DOCX, or TXT files"
    )
    
    # Create a temporary directory for storing documents if it doesn't exist
    temp_dir = "temp_docs"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    
    # Button to process and ingest the documents
    if st.button("Ingest Documents"):
        if uploaded_files:
            try:
                # Save uploaded files to temporary directory
                saved_files = []
                for uploaded_file in uploaded_files:
                    # Create temporary file path
                    temp_file_path = os.path.join(temp_dir, uploaded_file.name)
                    saved_files.append(temp_file_path)
                    
                    # Save uploaded file
                    with open(temp_file_path, "wb") as f:
                        f.write(uploaded_file.getvalue())
                
                # Process and ingest the documents
                with st.spinner("Processing documents..."):
                    process_pdfs_and_create_vectorstore_with_ai(
                        pdf_folder=temp_dir,
                        index_name=os.getenv("INDEX_NAME"),
                        namespace=os.getenv("NAMESPACE")
                    )
                ui.success(f"{len(saved_files)} document(s) successfully ingested!")
                
                # Clean up
                for file_path in saved_files:
                    if os.path.exists(file_path):
                        os.remove(file_path)
            
            except Exception as e:
                ui.error(f"Error processing documents: {str(e)}")
                # Clean up on error
                for file_path in saved_files:
                    if os.path.exists(file_path):
                        os.remove(file_path)
        else:
            st.warning("Please upload CV documents before ingesting.")

    # Add some information about supported formats
    st.markdown("""
    #### Supported Formats
    - PDF documents
    - DOCX documents
    - TXT documents
    
    #### Instructions
    1. Click 'Browse files' to select CV documents
    2. You can select multiple files at once
    3. Click 'Ingest Documents' to process and add them to the database
    """) 