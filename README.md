# DocuQuery with DialoGPT

A Document Query Assistant built with LangChain and Microsoft DialoGPT-large model. This tool allows you to upload documents (PDFs or URLs) and ask questions about their content using AI-powered search.

## Features

- **📄 Document Processing**: Load and process web URLs or PDF files
- **❓ Smart Q&A**: Ask natural language questions about document content
- **🔍 Source Tracking**: View which parts of the document were used to generate answers
- **🌐 Web Interface**: Simple and intuitive Streamlit web app
- **🔄 Vector Search**: Uses ChromaDB for efficient similarity search
- **🤖 Open-Source AI**: Powered by Microsoft's DialoGPT-large model

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step-by-Step Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/kanika-chauhan389/DocuQuery-DialoGPT.git
   cd DocuQuery-DialoGPT
2. **Create a virtual environment (recommended)**
   python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. **Install dependencies**
   pip install -r requirements.txt
   
### Usage
1. **Start the application**: streamlit run app.py
2. **Access the web interface**: Open your browser and go to http://localhost:8501
3. **Load a document**: Choose URL/PDF in sidebar → Enter URL or upload file → Click "Load Document"
4. **Ask questions**: Type question → View AI answer → Expand "View Source Documents" to see sources

### How it works
    1. Document Loading: The system loads documents from URLs or PDF files using LangChain's document loaders
    2. Text Splitting: Documents are split into smaller chunks for efficient processing
    3. Vector Storage: Text chunks are converted to vectors and stored in ChromaDB
    4. Query Processing: When you ask a question, it finds the most relevant text chunks
    5. Answer Generation: DialoGPT model generates answers based on the retrieved context
    6. Source Display: Shows you which document sections were used for the answer

### Example Use Cases
    1. Research: Ask questions about academic papers or articles
    2. Documentation: Query technical documentation or manuals
    3. Content Analysis: Extract insights from reports or blogs
    4. Study Aid: Quickly find information in educational materials

### Limitations
     1. DialoGPT may occasionally produce generic or repetitive responses
     2. Processing large documents may take time on CPU
     3. Web scraping depends on website accessibility and structure
     4. Better performance requires GPU acceleration
     5. Accuracy depends on the quality and relevance of the source document


  
