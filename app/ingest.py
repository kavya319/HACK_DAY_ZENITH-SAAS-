from langchain.document_loaders import PyPDFLoader
from langchain_qdrant import QdrantVectorStore
from langchain.embeddings import HuggingFaceEmbeddings
from utils import get_collection_name


def ingest_pdf(file_path: str, bot_id: str):
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    collection_name = get_collection_name(bot_id)

    QdrantVectorStore.from_documents(
        docs,
        embedding_model,
        url="http://localhost:6333",
        collection_name=collection_name
    )

    print(f"✅ Stored for bot: {bot_id}")