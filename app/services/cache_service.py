"""
Cache Service
Menyimpan hasil query agar tidak perlu memanggil LLM berulang kali
Menggunakan dictionary sederhana dengan TTL (Time To Live)
"""
import time
import hashlib
from typing import Optional, Dict, Any
from app.core.config import CACHE_ENABLED, CACHE_TTL

class CacheService:
    def __init__(self):
        """
        Inisialisasi cache storage
        cache_data: menyimpan {key: {"value": response, "timestamp": time}}
        """
        self.cache_data: Dict[str, Dict[str, Any]] = {}
    
    def _generate_key(self, question: str) -> str:
        """
        Generate unique key dari pertanyaan
        Menggunakan hash MD5 untuk membuat key yang konsisten
        """
        # Normalize: lowercase dan strip whitespace
        normalized = question.lower().strip()
        return hashlib.md5(normalized.encode()).hexdigest()
    
    def get(self, question: str) -> Optional[str]:
        """
        Mengambil jawaban dari cache jika ada dan belum expired
        Return None jika tidak ada atau sudah kadaluarsa
        """
        if not CACHE_ENABLED:
            return None
        
        key = self._generate_key(question)
        
        if key not in self.cache_data:
            return None
        
        cached_item = self.cache_data[key]
        current_time = time.time()
        
        # Check apakah cache sudah expired
        if current_time - cached_item["timestamp"] > CACHE_TTL:
            # Hapus cache yang sudah expired
            del self.cache_data[key]
            return None
        
        return cached_item["value"]
    
    def set(self, question: str, answer: str) -> None:
        """
        Menyimpan jawaban ke cache
        """
        if not CACHE_ENABLED:
            return
        
        key = self._generate_key(question)
        self.cache_data[key] = {
            "value": answer,
            "timestamp": time.time()
        }
    
    def clear(self) -> None:
        """
        Membersihkan seluruh cache
        """
        self.cache_data.clear()
    
    def stats(self) -> Dict[str, Any]:
        """
        Mengembalikan statistik cache
        """
        return {
            "total_cached": len(self.cache_data),
            "enabled": CACHE_ENABLED,
            "ttl_seconds": CACHE_TTL
        }

# Global cache instance
cache_service = CacheService()
