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
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config('RAG Application Demo')
st.header("Ask you question")
#OPENAI_API_KEY = st.text_input('OpenAI API Key', type='password')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
pdf_obj = st.file_uploader("Load your pdf files here", type="pdf", on_change=st.cache_resource.clear)

@st.cache_resource 
def create_embeddings(pdf):
    pdf_reader = PdfReader(pdf)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        length_function=len
        )        
    chunks = text_splitter.split_text(text)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    knowledge_base = FAISS.from_texts(chunks, embeddings)

    return knowledge_base
  
if pdf_obj:
    knowledge_base = create_embeddings(pdf_obj)
    
    # Initialize conversation memory
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    
    # Initialize the conversational chain
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model_name='gpt-3.5-turbo'),
        retriever=knowledge_base.as_retriever(),
        memory=memory
    )
    
    # Use session state to store and display chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "user_question" not in st.session_state:
        st.session_state.user_question = ""
    
    # Create a form for user input
    with st.form(key='question_form'):
        user_question = st.text_input("Haz una pregunta sobre tu PDF:", value=st.session_state.user_question)
        submit_button = st.form_submit_button("Consultar")

    if submit_button and user_question:
        os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
        response = qa_chain({"question": user_question})
        st.session_state.chat_history.append(("Human", user_question))
        st.session_state.chat_history.append(("AI", response['answer']))
        # Clear the input field
        st.session_state.user_question = ""
    elif submit_button and not user_question:
        st.warning("Por favor, introduce una pregunta.")

    # Add the "Start Over" button
    if st.button("Borrar historial"):
        st.session_state.chat_history = []
        st.session_state.user_question = ""
        st.rerun()

    # Display chat history
    for role, message in st.session_state.chat_history:
        st.write(f"{role}: {message}")