import chromadb
from chromadb.utils import embedding_functions

class VectorStoreBuilder:
    def __init__(self, documents, collection_name='your_collection_name'):
        self.documents = documents
        self.collection_name = collection_name
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(name=self.collection_name)

    def build_and_save(self):
        """Adds documents to the ChromaDB collection."""
        # Initialize the embedding function
        openai_ef = embedding_functions.OpenAIEmbeddingFunction(api_key='your_openai_api_key')

        # Assign the embedding function to the collection
        self.collection.modify(embedding_function=openai_ef)

        # Prepare data for insertion
        for idx, doc in enumerate(self.documents):
            self.collection.add(
                ids=[str(idx)],
                documents=[doc.page_content],
                metadatas=[doc.metadata]
            )
        print(f"Stored {len(self.documents)} documents in collection '{self.collection_name}'.")

# Usage example
vector_builder = VectorStoreBuilder(documents=markdown_processor.chunks, collection_name='bank_of_canada_reports')
vector_builder.build_and_save()
