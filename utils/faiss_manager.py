import faiss
import numpy as np
from typing import List, Tuple, Dict, Any
import pickle
import os

class FAISSManager:
    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
        self.metadata_store = []  # Store document metadata
        
        # Create data directory if it doesn't exist
        self.data_dir = "data"
        os.makedirs(self.data_dir, exist_ok=True)
        
        self.index_file = os.path.join(self.data_dir, "faiss_index.bin")
        self.metadata_file = os.path.join(self.data_dir, "metadata.pkl")
        
        # Load existing index if available
        self._load_index()
        
    def add_embeddings(self, embeddings: np.ndarray, metadata: List[Dict[str, Any]]):
        """
        Add embeddings and their metadata to the FAISS index.
        """
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(embeddings)
        
        # Add to index
        self.index.add(embeddings)
        
        # Store metadata
        self.metadata_store.extend(metadata)
        
        # Save to disk
        self._save_index()
        
    def search(self, query_embedding: np.ndarray, top_k: int = 3) -> List[Tuple[Dict[str, Any], float]]:
        """
        Search for similar embeddings and return metadata with scores.
        """
        if self.index.ntotal == 0:
            return []
            
        # Normalize query embedding
        query_embedding = query_embedding.reshape(1, -1).astype('float32')
        faiss.normalize_L2(query_embedding)
        
        # Search for more results to allow for deduplication
        search_k = min(top_k * 3, self.index.ntotal)
        scores, indices = self.index.search(query_embedding, search_k)
        
        # Deduplicate results by content similarity
        results = []
        seen_content = set()
        
        for score, idx in zip(scores[0], indices[0]):
            if idx != -1 and idx < len(self.metadata_store):
                metadata = self.metadata_store[idx]
                content = metadata['content']
                
                # Simple deduplication by checking if content is too similar
                content_key = content[:100].strip()  # Use first 100 chars as key
                
                if content_key not in seen_content and len(content.strip()) > 50:
                    results.append((metadata, float(score)))
                    seen_content.add(content_key)
                    
                    # Stop when we have enough unique results
                    if len(results) >= top_k:
                        break
                
        return results
        
    def _save_index(self):
        """
        Save FAISS index and metadata to disk.
        """
        try:
            # Save FAISS index
            faiss.write_index(self.index, self.index_file)
            
            # Save metadata
            with open(self.metadata_file, 'wb') as f:
                pickle.dump(self.metadata_store, f)
                
        except Exception as e:
            print(f"Error saving index: {e}")
            
    def _load_index(self):
        """
        Load FAISS index and metadata from disk.
        """
        try:
            if os.path.exists(self.index_file) and os.path.exists(self.metadata_file):
                # Load FAISS index
                self.index = faiss.read_index(self.index_file)
                
                # Load metadata
                with open(self.metadata_file, 'rb') as f:
                    self.metadata_store = pickle.load(f)
                    
                print(f"Loaded existing index with {self.index.ntotal} documents")
                
        except Exception as e:
            print(f"Error loading index: {e}")
            # Initialize fresh index if loading fails
            self.index = faiss.IndexFlatIP(self.dimension)
            self.metadata_store = []
            
    def get_stats(self) -> Dict[str, int]:
        """
        Get statistics about the index.
        """
        return {
            "total_documents": self.index.ntotal,
            "dimension": self.dimension,
            "metadata_count": len(self.metadata_store)
        }