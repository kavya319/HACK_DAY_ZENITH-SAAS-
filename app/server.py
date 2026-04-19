from fastapi import FastAPI, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import shutil
import uuid
import fitz  # PyMuPDF
import os

from langchain_qdrant import QdrantVectorStore
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

# ✅ CREATE APP FIRST
app = FastAPI()

# ✅ Mount static (for widget.js)
app.mount("/static", StaticFiles(directory="public"), name="static")

# ✅ Allow widget access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔹 Embedding model
embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-MiniLM-L3-v2"
)

# 🔹 ENV variables
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")


# 🔥 1. Create Bot
@app.post("/create-bot")
def create_bot():
    bot_id = str(uuid.uuid4())
    return {"bot_id": bot_id}


# 🔥 2. Upload PDF
@app.post("/upload")
def upload_pdf(
    bot_id: str = Query(...),
    file: UploadFile = File(...)
):
    file_path = f"temp_{file.filename}"

    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    docs = []

    # Extract text
    pdf = fitz.open(file_path)

    for page in pdf:
        text = page.get_text("text")

        if text:
            docs.append(Document(page_content=text.strip()))

    collection_name = f"bot_{bot_id}"

    # Store in Qdrant Cloud
    QdrantVectorStore.from_documents(
        docs,
        embedding,
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
        collection_name=collection_name
    )

    return {"status": "uploaded"}


# 🔥 3. Chat
@app.post("/chat")
def chat(
    query: str = Query(...),
    bot_id: str = Query(...)
):
    collection_name = f"bot_{bot_id}"

    try:
        vector_db = QdrantVectorStore.from_existing_collection(
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY,
            collection_name=collection_name,
            embedding=embedding
        )

        results = vector_db.similarity_search(query, k=3)

        context = "\n\n".join([doc.page_content for doc in results])

        if context:
            return {"reply": f"Based on document:\n{context[:500]}"}
        else:
            return {"reply": "I don't have information about that."}

    except Exception as e:
        return {"reply": f"Error: {str(e)}"}