from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import Runnable
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from typing import List
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Static and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Load models
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vector_store = FAISS.load_local("vectorstore/faiss_notes", embeddings, allow_dangerous_deserialization=True)
retriever = vector_store.as_retriever()
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# Global history
chat_history: List = []

# Prompt Template
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an academic assistant helping students by answering questions using their notes and previous year papers."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{question_with_context}")
])

# Chain
def get_chain() -> Runnable:
    return chat_prompt | llm

# Serve frontend
@app.get("/", response_class=HTMLResponse)
async def serve_ui(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# API schema
class QuestionRequest(BaseModel):
    query: str

class AnswerResponse(BaseModel):
    answer: str
    sources: List[str]

@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    # Retrieve docs
    docs = retriever.invoke(request.query)
    top_docs_text = "\n\n".join(doc.page_content for doc in docs[:3])
    sources = [doc.metadata.get("source", "Unknown") for doc in docs]

    # Compose input
    question_with_context = f"{request.query}\n\nContext:\n{top_docs_text}"
    input_data = {
        "question_with_context": question_with_context,
        "chat_history": chat_history
    }

    # Invoke LLM
    response = get_chain().invoke(input_data)

    # Update history
    chat_history.append(HumanMessage(content=request.query))
    chat_history.append(AIMessage(content=response.content))

    return AnswerResponse(answer=response.content, sources=sources)
