import streamlit as st
from utils import process_document, ask_question

st.set_page_config(page_title="DocuQuery-with-DailoGPT", page_icon="📄")
st.title("📄 DocuQuery with DialoGPT")

# Initialize session state
if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = None

# Sidebar for document input
with st.sidebar:  #
    st.header("Configure")
    doc_source = st.radio("Document Source:", ("URL", "PDF File"))

    if doc_source == "URL":
        document_input = st.text_input("Enter Document URL:")
        process_button = st.button("Load Document")
    else:
        document_input = st.file_uploader("Upload PDF", type="pdf")
        process_button = st.button("Load Document")

# Process document
if process_button and document_input:
    with st.spinner("Processing document....This may take a minute."):
        try:
            if doc_source == "URL":
                st.session_state.qa_chain = process_document(document_input, is_url=True)  # FIXED: False -> True
            else:
                # save the uploaded file temporarily
                with open("temp.pdf", "wb") as f:
                    f.write(document_input.getbuffer())
                st.session_state.qa_chain = process_document("temp.pdf", is_url=False)
            st.success("Document processed successfully!")  # FIXED: st.sucess -> st.success
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Main chat area
if st.session_state.qa_chain:
    st.header("Ask Questions about your document")  

    question = st.text_input("Enter your question:")
    if question:
        with st.spinner("Thinking...."):
            try:
                answer, sources = ask_question(st.session_state.qa_chain, question)

                st.subheader("Answer:")
                st.write(answer)

                with st.expander("View Source Documents"):  
                    for i, doc in enumerate(sources):
                        st.write(f"**Chunk {i+1}:** {doc.page_content[:200]}...")
            except Exception as e:
                st.error(f"Error answering question: {str(e)}")

else:
    st.info("👈 Please load a document from the sidebar to get started.")