from crewai.knowledge.embedder.base_embedder import BaseEmbedder

class CustomEmbedder(BaseEmbedder):
    def embed_chunks(self, chunks: List[str]) -> np.ndarray:
        # Your custom implementation here
        embeddings = np.array([len(chunk) for chunk in chunks])  # Example: using length as "embedding"
        return embeddings

    def embed_texts(self, texts: List[str]) -> np.ndarray:
        # Implement according to your needs
        return self.embed_chunks(texts)

    def embed_text(self, text: str) -> np.ndarray:
        # Implement for a single text
        return self.embed_chunks([text])[0]

    @property
    def dimension(self) -> int:
        # Return the dimensionality of your embeddings
        return 1
