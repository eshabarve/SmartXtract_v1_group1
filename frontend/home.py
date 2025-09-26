# importing Utilities
import time
import requests
import streamlit as st

st.set_page_config(page_title="SmartXtracts", layout="centered")

st.title("📄 SmartXtract")
st.caption("MVP - OCR + LLM Structuring App | Version 0")
st.divider()


# Drop Down Lists
col1, col2 = st.columns(2)

with col1:
    try:
        company_name = st.selectbox(
            label="Select Company",
            options=("ABC Ltd",),
            index=None,
            placeholder="Choose an option",
        )
    except Exception as e:
        st.error("Error while loading company list.")
        st.exception(e)

with col2:
    try:
        doc_type = st.selectbox(
            label="Select Document Type",
            options=("Invoice",),
            index=None,
            placeholder="Choose an option",
        )
    except Exception as e:
        st.error("Error while loading document types.")
        st.exception(e)


# Uploading Part
uploaded_file = st.file_uploader(
    label="Upload Image or PDF",
    type=["jpg", "jpeg", "png", "pdf"],
    accept_multiple_files=False,
)

if uploaded_file is not None:
    st.info(f"Uploaded file: {uploaded_file.name}")

    if st.button("Extract Data"):
        with st.spinner("🔍 Extracting data... please wait..."):
            try:
                # Validate dropdown selections before request
                if not company_name or not doc_type:
                    st.warning("Please select both Company and Document Type before extracting.")
                else:
                    try:
                        response = requests.post(
                            "http://127.0.0.1:5000",
                            files={"file": (uploaded_file.name, uploaded_file, uploaded_file.type)},
                            data={
                                "company_name": company_name,
                                "document_type": doc_type,
                            }
                        )
                    except requests.exceptions.ConnectionError:
                        st.error("Could not connect to backend server. Make sure Flask is running at http://127.0.0.1:5000.")
                    except requests.exceptions.Timeout:
                        st.error("Request timed out. Try again.")
                    except Exception as e:
                        st.error("Unexpected error while sending request.")
                        st.exception(e)
                    else:
                        # Handle response
                        if response.status_code == 200:
                            try:
                                result = response.json()
                                st.success("Extraction Successful")
                                st.json(result)
                            except Exception as e:
                                st.error("Failed to parse server response as JSON.")
                                st.text(response.text)  # show raw text for debugging
                                st.exception(e)
                        else:
                            st.error(f"Extraction Failed (Status: {response.status_code})")
                            st.text(response.text)

            except Exception as e:
                st.error("Something went wrong.")
                st.exception(e)
