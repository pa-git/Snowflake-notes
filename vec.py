from chromadb.config import Settings
import chromadb

BATCH_SIZE = 300

class VectorStoreBuilder:
    def __init__(self, documents, collection_name):
        self.collection_name = collection_name
        self.db_path = f"/d/d1/genai/vector_store/{collection_name}"
        self.documents = documents

        print(f"Total Documents: {len(self.documents)}")

        self.client = chromadb.PersistentClient(
            path=self.db_path,
            settings=Settings(
                anonymized_telemetry=False,
                persist_directory=self.db_path
            )
        )
        self.collection = self.client.create_collection(name=self.collection_name)

    def build_and_save(self):
        """Adds documents in batches to the ChromaDB collection."""
        total = len(self.documents)

        for start in range(0, total, BATCH_SIZE):
            end = min(start + BATCH_SIZE, total)
            batch_docs = self.documents[start:end]

            docs_text = [doc.page_content for doc in batch_docs]
            docs_metadata = [doc.metadata for doc in batch_docs]
            doc_ids = [str(i) for i in range(start, end)]

            embeddings = gpt.generate_embeddings_scalar2(docs_text)

            print(f"Processed batch {start}–{end} | Embeddings: {len(embeddings)}")

            self.collection.add(
                documents=docs_text,
                embeddings=embeddings,
                metadatas=docs_metadata,
                ids=doc_ids
            )

        print(f"✅ Stored {total} documents in persistent collection '{self.collection_name}' at '{self.db_path}'")
