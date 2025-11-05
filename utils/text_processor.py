import re
from typing import List

class TextProcessor:
    def __init__(self):
        self.chunk_size = 300  # Reduced for better semantic chunks
        self.overlap = 30      # Reduced overlap
        
    def chunk_text(self, text: str, language: str = 'en') -> List[str]:
        """
        Split text into meaningful semantic chunks for better retrieval.
        """
        # Clean the text
        text = self._clean_text(text)
        
        # First try to split by paragraphs or sections
        paragraphs = self._split_by_paragraphs(text)
        
        chunks = []
        for paragraph in paragraphs:
            if len(paragraph) <= self.chunk_size:
                if paragraph.strip():
                    chunks.append(paragraph.strip())
            else:
                # Split large paragraphs into sentences
                sentences = self._split_by_sentences(paragraph, language)
                current_chunk = ""
                
                for sentence in sentences:
                    # If adding this sentence would exceed chunk size, save current chunk
                    if len(current_chunk) + len(sentence) > self.chunk_size and current_chunk:
                        chunks.append(current_chunk.strip())
                        current_chunk = sentence
                    else:
                        current_chunk += " " + sentence if current_chunk else sentence
                
                # Add the last chunk
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())
        
        # Remove duplicates and very short chunks
        unique_chunks = []
        seen = set()
        for chunk in chunks:
            chunk_clean = chunk.strip()
            if len(chunk_clean) > 50 and chunk_clean not in seen:  # Minimum 50 chars
                unique_chunks.append(chunk_clean)
                seen.add(chunk_clean)
                
        return unique_chunks
    
    def _split_by_paragraphs(self, text: str) -> List[str]:
        """Split text by paragraphs or numbered sections."""
        # Split by double newlines (paragraphs)
        paragraphs = re.split(r'\n\s*\n', text)
        
        # Also split by numbered sections (1., 2., etc.)
        all_sections = []
        for para in paragraphs:
            sections = re.split(r'(?=\d+\.\s)', para)
            all_sections.extend([s.strip() for s in sections if s.strip()])
            
        return all_sections
    
    def _split_by_sentences(self, text: str, language: str) -> List[str]:
        """Split text into sentences based on language."""
        if language == 'ja':
            # Japanese sentence endings
            sentences = re.split(r'[。！？]', text)
        else:
            # English sentence endings
            sentences = re.split(r'[.!?]+\s+', text)
            
        return [s.strip() for s in sentences if s.strip()]
        
    def _clean_text(self, text: str) -> str:
        """
        Clean and normalize text.
        """
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s\.\!\?\,\;\:\-\(\)\[\]\{\}\"\'。！？、；：（）［］｛｝「」『』]', '', text)
        
        return text.strip()