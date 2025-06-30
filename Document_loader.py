from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize model and embedding
model = ChatGoogleGenerativeAI(model='models/chat-001')
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Load PDFs from directory
loader = DirectoryLoader(
    path='allpdfs',
    glob='*.pdf',
    loader_cls=PyPDFLoader
)
docs = loader.load()

# Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=2000,
    chunk_overlap=200,
    separators=["\n\n", "\n", " ", ""]
)
chunks = text_splitter.split_documents(docs)

# Create FAISS vectorstore and save to disk
vector_store = FAISS.from_documents(chunks, embeddings)
vector_store.save_local("vectorstore/faiss_notes")

vector_store = FAISS.load_local(
    "vectorstore/faiss_notes",
    embeddings,
    allow_dangerous_deserialization=True
)

# Create retriever
retriever = vector_store.as_retriever()
