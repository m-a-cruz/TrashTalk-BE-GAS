from haystack.document_stores import FAISSDocumentStore
from haystack.nodes import EmbeddingRetriever, TransformersSummarizer
from pymongo import MongoClient
import pandas as pd

# 1. Mongo → DataFrame -------------------------------------------------
client = MongoClient("mongodb+srv://yanie:qM0somsYwQXQEM9P@cluster0.qarpj.mongodb.net/?retryWrites=true&w=majority&tls=true")
db  = client["trashTalk"]

predictions = list(db["predictions"].find({}).sort("timestamp", -1).limit(5))
df = pd.DataFrame(predictions).astype({"predicted_value": float})
df["timestamp"] = pd.to_datetime(df["timestamp"])
df.sort_values("timestamp", inplace=True)

# 2. Convert to Haystack docs -----------------------------------------
docs = [
    {"content": f"Date: {r.timestamp}, LEL: {r.predicted_value:.2f}, Gas: {r.gas_type}, Type: {r.type}"}
    for r in df.itertuples()
]

# 3. Vector store 384-dim (MiniLM) ------------------------------------
document_store = FAISSDocumentStore(faiss_index_factory_str="Flat",
                                    embedding_dim=384,   # <-- matches MiniLM
                                    sql_url="sqlite://")  # in-memory; no sync woes
document_store.write_documents(docs)

retriever = EmbeddingRetriever(document_store=document_store,
                               embedding_model="sentence-transformers/all-MiniLM-L6-v2",
                               use_gpu=False)

document_store.update_embeddings(retriever)

# 4. ► LIGHTWEIGHT summariser instead of BART-large-cnn ◄ -------------
#   DistilBART is 4 × smaller and works fine on a laptop CPU
summarizer = TransformersSummarizer(
    model_name_or_path="sshleifer/distilbart-cnn-12-6",
    use_auth_token=None,
)

# 5. Run the summary ---------------------------------------------------
all_docs = document_store.get_all_documents()        # returns Haystack Document objects
summary  = summarizer.predict(documents=all_docs)    # returns list[str]

print("\nSummary:\n", summary[0])


# print("\n📊 Summary of gas concentration data:")
# print(summary[0])
