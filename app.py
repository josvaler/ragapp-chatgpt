# Import necessary libraries
import streamlit as st
import os
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings 
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up Streamlit page configuration
st.set_page_config('RAG')
st.header("Preguntar a tu PDF")

# Get OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Create a file uploader for PDF files
pdf_obj = st.file_uploader("Carga tus archivos pdf", type="pdf", on_change=st.cache_resource.clear)

# Function to create embeddings from PDF content
@st.cache_resource 
def create_embeddings(pdf):
    # Extract text from PDF
    pdf_reader = PdfReader(pdf)
    text = "".join(page.extract_text() for page in pdf_reader.pages)

    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        length_function=len
    )        
    chunks = text_splitter.split_text(text)

    # Create embeddings and knowledge base
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    knowledge_base = FAISS.from_texts(chunks, embeddings)

    return knowledge_base

# Initialize session state variables
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "user_question" not in st.session_state:
    st.session_state.user_question = ""

# Main application logic
if pdf_obj:
    # Create knowledge base from PDF
    knowledge_base = create_embeddings(pdf_obj)
    
    # Initialize conversation memory
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    
    # Initialize the conversational chain
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model_name='gpt-3.5-turbo'),
        retriever=knowledge_base.as_retriever(),
        memory=memory
    )

    # Function to handle question submission
    def submit():
        st.session_state.user_question = st.session_state.temp_question
        st.session_state.temp_question = ""

    # Create input field for user questions
    input_container = st.empty()
    user_question = input_container.text_input("Preguntar a tu PDF:", key="temp_question")

    # Handle question submission
    if st.button("Consultar", on_click=submit):
        if st.session_state.user_question:
            os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
            
            # Get response from the QA chain
            response = qa_chain({"question": st.session_state.user_question})
            
            # Update chat history
            st.session_state.chat_history.append(("Human", st.session_state.user_question))
            st.session_state.chat_history.append(("AI", response['answer']))
            
            # Clear the input field
            st.session_state.user_question = ""
        else:
            st.warning("Por favor, ingrese una pregunta.")

# Display chat history
for role, message in st.session_state.chat_history:
    st.write(f"{role}: {message}")

if len(st.session_state.chat_history) > 0:
    if st.button("Borrar historial"):
            st.session_state.chat_history = []
            st.rerun()
