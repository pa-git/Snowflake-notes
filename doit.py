import chromadb
from chromadb.utils import embedding_functions

class VectorStoreBuilder:
    def __init__(self, documents, collection_name='your_collection_name', db_path='db_2'):
        self.documents = documents
        self.collection_name = collection_name
        # Persistent ChromaDB client
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(name=self.collection_name)

    def build_and_save(self):
        """Adds documents with embeddings into the ChromaDB collection."""
        # Initialize OpenAI embedding function (ensure API key is set in your environment)
        openai_ef = embedding_functions.OpenAIEmbeddingFunction(api_key='your_openai_api_key')

        # Assign embedding function to the collection
        self.collection.modify(embedding_function=openai_ef)

        # Prepare and insert documents
        for idx, doc in enumerate(self.documents):
            self.collection.add(
                ids=[str(idx)],
                documents=[doc.page_content],
                metadatas=[doc.metadata]
            )
        print(f"Stored {len(self.documents)} documents in persistent collection '{self.collection_name}' at '{self.client._settings.persist_directory}'.")

# Usage example:
vector_builder = VectorStoreBuilder(
    documents=markdown_processor.chunks, 
    collection_name='bank_of_canada_reports',
    db_path='db_2'
)
vector_builder.build_and_save()
