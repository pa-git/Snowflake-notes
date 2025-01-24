# Core libraries
numpy>=1.21.0
pandas>=1.3.0
jsonlines>=2.0.0

# TM1py for connecting to TM1
tm1py>=1.8.0

# Sentence Transformers for generating text embeddings
sentence-transformers>=2.2.0

# faiss for building and querying indices
# If you do not have GPU support, use faiss-cpu instead of faiss-gpu.
faiss-cpu>=1.7.2

# PyTorch is required by sentence-transformers
# Adjust the version based on CUDA or CPU requirements
torch>=1.10.0
