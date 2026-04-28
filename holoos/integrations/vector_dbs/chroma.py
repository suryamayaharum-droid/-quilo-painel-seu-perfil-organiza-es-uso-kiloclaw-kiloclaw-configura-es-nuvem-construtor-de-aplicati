"""
HoloOS ChromaDB Integration
============================
Integração com ChromaDB para vetorização e busca.
"""

from typing import List, Dict, Any, Optional
import logging
import numpy as np

logger = logging.getLogger(__name__)

try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False
    logger.warning("ChromaDB not installed. Install with: pip install chromadb")


class ChromaDBVectorStore:
    """
    Vector store baseado em ChromaDB.
    
    Substitui ou complementa o VectorStore nativo do HoloOS RAG.
    """
    
    def __init__(
        self,
        collection_name: str = "holoos_documents",
        persist_directory: Optional[str] = None,
        dimension: int = 768
    ):
        """
        Inicializa conexão com ChromaDB.
        
        Args:
            collection_name: Nome da coleção
            persist_directory: Diretório para persistência (opcional)
            dimension: Dimensão dos embeddings
        """
        if not CHROMADB_AVAILABLE:
            raise ImportError("ChromaDB not available")
        
        self.dimension = dimension
        self.collection_name = collection_name
        
        # Configura cliente
        if persist_directory:
            self.client = chromadb.PersistentClient(path=persist_directory)
        else:
            self.client = chromadb.Client()
        
        # Cria ou obtém coleção
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}  # Similaridade por cosseno
        )
        
        logger.info(f"ChromaDB initialized: {collection_name}")
    
    def add(
        self,
        documents: List[str],
        embeddings: Optional[List[List[float]]] = None,
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None
    ) -> List[str]:
        """
        Adiciona documentos à coleção.
        
        Args:
            documents: Lista de textos
            embeddings: Embeddings pré-calculados (opcional)
            metadatas: Metadados associados
            ids: IDs únicos para documentos
            
        Returns:
            Lista de IDs adicionados
        """
        if ids is None:
            ids = [f"doc_{i}" for i in range(len(documents))]
        
        # Prepara dados
        add_kwargs = {
            "documents": documents,
            "ids": ids
        }
        
        if embeddings:
            add_kwargs["embeddings"] = embeddings
        
        if metadatas:
            add_kwargs["metadatas"] = metadatas
        
        self.collection.add(**add_kwargs)
        logger.info(f"Added {len(documents)} documents to ChromaDB")
        
        return ids
    
    def search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Busca documentos similares.
        
        Args:
            query_embedding: Embedding da query
            top_k: Número de resultados
            filter_metadata: Filtro por metadados
            
        Returns:
            Lista de documentos com scores
        """
        query_kwargs = {
            "query_embeddings": [query_embedding],
            "n_results": top_k
        }
        
        if filter_metadata:
            query_kwargs["where"] = filter_metadata
        
        results = self.collection.query(**query_kwargs)
        
        # Formata resultados
        formatted = []
        if results["documents"] and results["documents"][0]:
            for i, doc in enumerate(results["documents"][0]):
                formatted.append({
                    "content": doc,
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    "score": 1 - results["distances"][0][i] if results["distances"] else 0.0,
                    "id": results["ids"][0][i]
                })
        
        return formatted
    
    def delete(self, ids: List[str]) -> None:
        """Remove documentos por ID."""
        self.collection.delete(ids=ids)
        logger.info(f"Deleted {len(ids)} documents")
    
    def count(self) -> int:
        """Retorna número de documentos."""
        return self.collection.count()
    
    def clear(self) -> None:
        """Limpa toda a coleção."""
        self.client.delete_collection(self.collection_name)
        logger.info("Collection cleared")


class ChromaDBRAGEngine:
    """
    Motor RAG usando ChromaDB como backend.
    """
    
    def __init__(
        self,
        collection_name: str = "holoos_rag",
        persist_directory: Optional[str] = None,
        embedding_function: Optional[Any] = None
    ):
        """
        Inicializa motor RAG com ChromaDB.
        
        Args:
            collection_name: Nome da coleção
            persist_directory: Diretório para persistência
            embedding_function: Função de embedding (usa default se None)
        """
        if not CHROMADB_AVAILABLE:
            raise RuntimeError("ChromaDB not available")
        
        self.vector_store = ChromaDBVectorStore(
            collection_name=collection_name,
            persist_directory=persist_directory
        )
        
        # Usa embedding function do ChromaDB ou customizada
        self.embedding_function = embedding_function
        
        logger.info("ChromaDB RAG Engine initialized")
    
    def add_document(
        self,
        content: str,
        metadata: Dict[str, Any] = None
    ) -> str:
        """Adiciona um documento."""
        doc_id = f"doc_{self.vector_store.count()}"
        
        add_kwargs = {
            "documents": [content],
            "ids": [doc_id]
        }
        
        if metadata:
            add_kwargs["metadatas"] = [metadata]
        
        self.vector_store.collection.add(**add_kwargs)
        return doc_id
    
    def add_documents(self, documents: List[Dict[str, Any]]) -> List[str]:
        """Adiciona múltiplos documentos."""
        contents = [doc.get("content", "") for doc in documents]
        metadatas = [doc.get("metadata", {}) for doc in documents]
        ids = [f"doc_{i}" for i in range(len(contents))]
        
        self.vector_store.add(
            documents=contents,
            metadatas=metadatas,
            ids=ids
        )
        
        return ids
    
    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        query_embedding: Optional[List[float]] = None
    ) -> List[Dict[str, Any]]:
        """
        Recupera documentos relevantes.
        
        Args:
            query: Texto da query
            top_k: Número de resultados
            query_embedding: Embedding pré-calculado (opcional)
            
        Returns:
            Lista de documentos recuperados
        """
        # Gera embedding se não fornecido
        if query_embedding is None:
            # Usa embedding simples baseado em hash (substituir por modelo real)
            query_embedding = self._simple_embedding(query)
        
        return self.vector_store.search(query_embedding, top_k=top_k)
    
    def _simple_embedding(self, text: str) -> List[float]:
        """Gera embedding simples (placeholder)."""
        # Em produção, usar modelo real como sentence-transformers
        np.random.seed(hash(text) % 10000)
        embedding = np.random.randn(768)
        embedding = embedding / np.linalg.norm(embedding)
        return embedding.tolist()
    
    def generate_context(self, query: str, max_docs: int = 3) -> str:
        """Gera contexto a partir de documentos recuperados."""
        results = self.retrieve(query, top_k=max_docs)
        
        context_parts = []
        for result in results:
            context_parts.append(result.get("content", ""))
        
        return "\n\n".join(context_parts)
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do RAG."""
        return {
            "total_documents": self.vector_store.count(),
            "backend": "chromadb",
            "collection": self.vector_store.collection_name
        }


def get_chromadb_rag(
    collection_name: str = "holoos_rag",
    persist_directory: Optional[str] = None
) -> ChromaDBRAGEngine:
    """Factory function para criar engine RAG com ChromaDB."""
    return ChromaDBRAGEngine(
        collection_name=collection_name,
        persist_directory=persist_directory
    )


__all__ = [
    "ChromaDBVectorStore",
    "ChromaDBRAGEngine",
    "get_chromadb_rag"
]
