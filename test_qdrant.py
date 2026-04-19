from langchain_qdrant import QdrantVectorStore
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
# 🔹 Free embedding model
embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 🔹 Sample data (your "PDF chunks")
docs = [
    Document(page_content="Pricing is 1000 rupees per month"),
    Document(page_content="Refund policy allows returns within 7 days"),
    Document(page_content="Support is available 24/7 via chat")
]

# 🔹 Store in Qdrant
vector_db = QdrantVectorStore.from_documents(
    docs,
    embedding,
    url="http://localhost:6333",
    collection_name="test_collection"
)

print("✅ Data stored in Qdrant")

# 🔹 Query test
query = "What is the price?"

results = vector_db.similarity_search(query, k=2)

print("\n🔍 Results:")
for r in results:
    print("-", r.page_content)