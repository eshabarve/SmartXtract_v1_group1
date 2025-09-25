# importing  Utilities
import streamlit as st
import requests

st.set_page_config(page_title="SmartXtracts", layout="centered")

st.title("📄 SmartXtract")
st.caption("MVP - OCR + LLM Structuring App | Version 0")
st.divider()


# Drop Down Lists
col1, col2 = st.columns(2)

with col1:
     company_name = st.selectbox(
     label="Select Company",
     options=("ABC Ltd"),
     index=None,
     placeholder="Choose an option",
     )

with col2:
     doc_type = st.selectbox(
     label="Select Document Type",
     options=("Invoice"),
     index=None,
     placeholder="Choose an option",
     )


# Uploading Part
uploaded_file = st.file_uploader(
     label="Upload Image or PDF",
     type=["jpg", "jpeg", "png", "pdf"],
     accept_multiple_files = False, 
     )

if uploaded_file is not None:
    st.info(f"Uploaded file")

    if st.button("Extract Data"):
        # Show spinner while backend works
        with st.spinner("🔍 Extracting data... please wait..."):
            try:                
                response = requests.post(
                "http://127.0.0.1:5000",
                files={"file": uploaded_file.getvalue()},
                data={
                    "company_name": company_name,
                    "document_type": doc_type,
                }
            )
                if response.status_code == 200:
                    result = response.json()
                    st.success("Extraction Successful")
                    st.json(result)
                else:
                    st.error("Extraction Failed")
            except Exception as e:
                st.error(f"Error: {e}")

# Save Uploaded Files

# if uploaded_file is not None:
#      saved_path = save_uploaded_path()