from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load FAISS vectorstore and embeddings
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vector_store = FAISS.load_local(
    "vectorstore/faiss_notes",
    embeddings,
    allow_dangerous_deserialization=True
)

# Create retriever
retriever = vector_store.as_retriever()

# Load LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# RAG chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff",  # 'stuff' = simple combine; later we can use 'map_reduce' or 'refine'
    return_source_documents=True  # Optional: lets you see which docs were used
)

# Example query
query = "What is capital of india?"
response = qa_chain.invoke({"query": query})

print("Answer:", response["result"])
print("\nSources:")
for doc in response["source_documents"]:
    print("-", doc.metadata.get("source", "Unknown"))
