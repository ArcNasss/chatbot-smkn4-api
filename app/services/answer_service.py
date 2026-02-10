"""
Answer Service
Orchestrator utama yang menggabungkan cache, retrieval, dan LLM
Menggunakan hybrid approach: direct answer → cache → LLM
"""
from typing import Dict, Any
from app.core.llm import llm
from app.core.config import SYSTEM_PROMPT
from app.services.cache_service import cache_service
from app.services.retrieval_service import retrieval_service

class AnswerService:
    def __init__(self):
        """
        Initialize dengan semua services yang dibutuhkan
        """
        self.llm = llm
        self.cache = cache_service
        self.retrieval = retrieval_service
        
        # Tracking untuk monitoring
        self.stats = {
            "total_questions": 0,
            "direct_answers": 0,
            "cache_hits": 0,
            "llm_calls": 0,
            "no_context_found": 0
        }
    
    def get_answer(self, question: str) -> Dict[str, Any]:
        """
        Main method untuk mendapatkan jawaban
        Flow: Direct Answer → Cache → LLM → Fallback
        
        Return: {
            "jawaban": str,
            "source": "direct" | "cache" | "llm" | "fallback",
            "metadata": {...}
        }
        """
        self.stats["total_questions"] += 1
        
        # STEP 1: Coba direct answer (tanpa LLM)
        direct_answer = self.retrieval.get_direct_answer(question)
        if direct_answer:
            self.stats["direct_answers"] += 1
            return {
                "jawaban": direct_answer,
                "source": "direct",
                "metadata": {
                    "llm_used": False,
                    "tokens_saved": "~500"  # Estimasi token yang dihemat
                }
            }
        
        # STEP 2: Check cache
        cached_answer = self.cache.get(question)
        if cached_answer:
            self.stats["cache_hits"] += 1
            return {
                "jawaban": cached_answer,
                "source": "cache",
                "metadata": {
                    "llm_used": False,
                    "tokens_saved": "~300"
                }
            }
        
        # STEP 3: Retrieve relevant data
        retrieved_data = self.retrieval.retrieve_relevant_data(question)
        
        # STEP 4: Panggil LLM dengan atau tanpa context
        if not retrieved_data:
            # Tidak ada context spesifik, tapi coba jawab dengan pengetahuan umum
            self.stats["no_context_found"] += 1
            answer = self._call_llm_general(question)
        else:
            # Ada context relevan
            context = self.retrieval.format_context(retrieved_data)
            answer = self._call_llm(question, context)
            self.stats["llm_calls"] += 1
        
        # Cache hasil
        self.cache.set(question, answer)
        
        return {
            "jawaban": answer,
            "source": "llm",
            "metadata": {
                "llm_used": True,
                "context_available": retrieved_data is not None,
                "context_length": len(self.retrieval.format_context(retrieved_data)) if retrieved_data else 0
            }
        }
    
    def _call_llm(self, question: str, context: str) -> str:
        """
        Memanggil LLM dengan context dari data sekolah
        """
        prompt = f"""{SYSTEM_PROMPT}

Data sekolah:
{context}

Pertanyaan: {question}

Jawab dengan gaya natural dan informatif:"""
        
        try:
            response = self.llm.invoke(prompt)
            return response.content.strip()
        except Exception as e:
            error_message = str(e)
            
            if "rate_limit_exceeded" in error_message.lower() or "429" in error_message:
                return "Maaf, batas penggunaan API tercapai. Silakan coba lagi nanti."
            
            return "Maaf, terjadi kesalahan saat memproses pertanyaan."
    
    def _call_llm_general(self, question: str) -> str:
        """
        Memanggil LLM tanpa context spesifik
        Untuk pertanyaan yang tidak ada di data tapi masih relevan dengan sekolah
        """
        prompt = f"""{SYSTEM_PROMPT}

Pertanyaan: {question}

Catatan: Jika pertanyaan tentang SMKN 4 Bojonegoro tapi tidak ada data spesifik, jawab dengan pengetahuan umum tentang SMK atau topik terkait. Jika benar-benar tidak relevan dengan sekolah, beritahu dengan sopan dan sarankan topik yang bisa ditanyakan.

Jawab:"""
        
        try:
            response = self.llm.invoke(prompt)
            return response.content.strip()
        except Exception as e:
            error_message = str(e)
            
            if "rate_limit_exceeded" in error_message.lower() or "429" in error_message:
                return "Maaf, batas penggunaan API tercapai. Silakan coba lagi nanti."
            
            return "Maaf, pertanyaan Anda di luar cakupan informasi yang saya miliki tentang SMKN 4 Bojonegoro. Silakan tanyakan tentang profil sekolah, jurusan, fasilitas, atau hal terkait SMK."
    
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Mengembalikan statistik penggunaan
        Berguna untuk monitoring efisiensi
        """
        total = self.stats["total_questions"]
        if total == 0:
            return self.stats
        
        return {
            **self.stats,
            "efficiency": {
                "direct_answer_rate": f"{(self.stats['direct_answers'] / total) * 100:.1f}%",
                "cache_hit_rate": f"{(self.stats['cache_hits'] / total) * 100:.1f}%",
                "llm_usage_rate": f"{(self.stats['llm_calls'] / total) * 100:.1f}%",
                "token_saving_rate": f"{((self.stats['direct_answers'] + self.stats['cache_hits']) / total) * 100:.1f}%"
            }
        }
    
    def reset_stats(self) -> None:
        """
        Reset statistik
        """
        for key in self.stats:
            self.stats[key] = 0

# Global answer service instance
answer_service = AnswerService()
