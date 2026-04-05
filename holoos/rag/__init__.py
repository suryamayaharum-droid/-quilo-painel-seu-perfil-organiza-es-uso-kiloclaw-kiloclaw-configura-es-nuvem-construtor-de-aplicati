"""
HoloOS RAG System
==================
Retrieval-Augmented Generation with embeddings.
"""

import numpy as np
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class Document:
    id: str
    content: str
    embedding: Optional[np.ndarray] = None
    metadata: Dict[str, Any] = None
    score: float = 0.0


class EmbeddingGenerator:
    def __init__(self, dimension: int = 768):
        self.dimension = dimension
    
    def generate(self, text: str) -> np.ndarray:
        hash_val = hash(text) % 10000
        np.random.seed(hash_val)
        embedding = np.random.randn(self.dimension)
        embedding = embedding / np.linalg.norm(embedding)
        return embedding
    
    def generate_batch(self, texts: List[str]) -> List[np.ndarray]:
        return [self.generate(text) for text in texts]


class VectorStore:
    def __init__(self, dimension: int = 768):
        self.dimension = dimension
        self.documents: List[Document] = []
    
    def add(self, document: Document):
        self.documents.append(document)
    
    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> List[Document]:
        results = []
        
        for doc in self.documents:
            if doc.embedding is not None:
                similarity = np.dot(query_embedding, doc.embedding)
                doc.score = float(similarity)
                results.append(doc)
        
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:top_k]
    
    def count(self) -> int:
        return len(self.documents)


class RAGEngine:
    def __init__(self):
        self.embedding_generator = EmbeddingGenerator()
        self.vector_store = VectorStore()
    
    def add_document(self, content: str, metadata: Dict[str, Any] = None):
        embedding = self.embedding_generator.generate(content)
        doc = Document(
            id=f"doc_{len(self.vector_store.documents)}",
            content=content,
            embedding=embedding,
            metadata=metadata or {}
        )
        self.vector_store.add(doc)
        return doc.id
    
    def add_documents(self, documents: List[Dict[str, Any]]):
        ids = []
        for doc in documents:
            content = doc.get("content", "")
            metadata = doc.get("metadata", {})
            doc_id = self.add_document(content, metadata)
            ids.append(doc_id)
        return ids
    
    def retrieve(self, query: str, top_k: int = 5) -> List[Document]:
        query_embedding = self.embedding_generator.generate(query)
        results = self.vector_store.search(query_embedding, top_k)
        return results
    
    def generate_context(self, query: str, max_docs: int = 3) -> str:
        results = self.retrieve(query, top_k=max_docs)
        context_parts = []
        for doc in results:
            context_parts.append(doc.content)
        return "\n\n".join(context_parts)
    
    def answer(self, query: str, base_response: str = "") -> Dict[str, Any]:
        context = self.generate_context(query)
        retrieval_results = self.retrieve(query)
        
        return {
            "query": query,
            "answer": f"{base_response or 'Based on retrieved context:'}\n\n{context[:200]}...",
            "sources": [doc.id for doc in retrieval_results],
            "retrieved_count": len(retrieval_results),
        }
    
    def get_stats(self) -> Dict[str, Any]:
        return {
            "total_documents": self.vector_store.count(),
            "dimension": self.vector_store.dimension,
            "indexed": True,
        }


def get_rag_engine() -> RAGEngine:
    return RAGEngine()


__all__ = ["RAGEngine", "VectorStore", "EmbeddingGenerator", "Document", "get_rag_engine"]