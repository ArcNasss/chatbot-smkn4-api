"""
Retrieval Service
Mengambil hanya data yang relevan dari JSON berdasarkan pertanyaan
Menggunakan keyword matching untuk efisiensi
"""
import json
import os
from typing import Dict, List, Any, Optional
from app.core.config import MAX_CONTEXT_LENGTH

class RetrievalService:
    def __init__(self, data_path: str = "data/info_sekolah.json"):
        """
        Load data sekolah dari JSON
        """
        self.data_path = data_path
        self.data = self._load_data()
        
        # Mapping keyword ke section data
        self.keyword_mapping = {
            # Profile sekolah
            "nama": ["profile", "nama"],
            "alamat": ["profile", "alamat"],
            "lokasi": ["profile", "alamat"],
            "kepala sekolah": ["profile", "kepala_sekolah"],
            "kepsek": ["profile", "kepala_sekolah"],
            "siswa": ["profile", "jumlah_siswa"],
            "murid": ["profile", "jumlah_siswa"],
            "guru": ["profile", "jumlah_guru"],
            "pengajar": ["profile", "jumlah_guru"],
            "akreditasi": ["profile", "akreditasi"],
            "visi": ["profile", "visi"],
            "misi": ["profile", "misi"],
            "profile": ["profile"],
            "profil": ["profile"],
            "sejarah": ["profile"],
            
            # Jurusan
            "jurusan": ["jurusan"],
            "tkj": ["jurusan", "TKJ"],
            "rekayasa perangkat lunak": ["jurusan", "RPL"],
            "rpl": ["jurusan", "RPL"],
            "multimedia": ["jurusan", "MM"],
            "mm": ["jurusan", "MM"],
            "teknik komputer": ["jurusan", "TKJ"],
            "jaringan": ["jurusan", "TKJ"],
            "software": ["jurusan", "RPL"],
            "aplikasi": ["jurusan", "RPL"],
            "desain": ["jurusan", "MM"],
            "video": ["jurusan", "MM"],
            "animasi": ["jurusan", "MM"],
            
            # Fasilitas
            "fasilitas": ["fasilitas"],
            "lab": ["fasilitas"],
            "laboratorium": ["fasilitas"],
            "perpustakaan": ["fasilitas"],
            "masjid": ["fasilitas"],
            "wifi": ["fasilitas"],
            "internet": ["fasilitas"],
            "komputer": ["fasilitas"],
            "gedung": ["fasilitas"],
            "ruang": ["fasilitas"],
        }
    
    def _load_data(self) -> Dict[str, Any]:
        """
        Load JSON data dari file
        """
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: File {self.data_path} tidak ditemukan")
            return {}
    
    def _get_nested_value(self, data: Dict, keys: List[str]) -> Any:
        """
        Mengambil nilai nested dari dictionary
        Contoh: keys=["profile", "nama"] -> data["profile"]["nama"]
        """
        current = data
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return None
        return current
    
    def retrieve_relevant_data(self, question: str) -> Optional[Dict[str, Any]]:
        """
        Mengambil data yang relevan berdasarkan pertanyaan
        Return: {"section": "...", "data": {...}, "direct_answer": "..."}
        """
        question_lower = question.lower()
        
        # Cari keyword yang cocok
        matched_sections = []
        for keyword, path in self.keyword_mapping.items():
            if keyword in question_lower:
                value = self._get_nested_value(self.data, path)
                if value is not None:
                    matched_sections.append({
                        "keyword": keyword,
                        "path": path,
                        "data": value
                    })
        
        if not matched_sections:
            return None
        
        # Ambil section pertama yang match (paling relevan)
        return matched_sections[0]
    
    def format_context(self, retrieved_data: Dict[str, Any]) -> str:
        """
        Format data yang sudah di-retrieve menjadi context string
        Batasi panjang sesuai MAX_CONTEXT_LENGTH
        """
        if not retrieved_data:
            return ""
        
        data = retrieved_data.get("data")
        keyword = retrieved_data.get("keyword", "")
        
        # Format berdasarkan tipe data
        if isinstance(data, dict):
            # Jika dict, ambil key-value yang penting
            context_parts = []
            for key, value in data.items():
                if isinstance(value, (str, int, float)):
                    context_parts.append(f"{key}: {value}")
                elif isinstance(value, list):
                    context_parts.append(f"{key}: {', '.join(map(str, value))}")
            context = " | ".join(context_parts)
        elif isinstance(data, list):
            context = ", ".join(map(str, data))
        else:
            context = str(data)
        
        # Potong jika terlalu panjang
        if len(context) > MAX_CONTEXT_LENGTH:
            context = context[:MAX_CONTEXT_LENGTH] + "..."
        
        return context
    
    def get_direct_answer(self, question: str) -> Optional[str]:
        """
        Coba jawab langsung tanpa LLM untuk pertanyaan sederhana
        Return None jika perlu LLM untuk penjelasan lebih detail
        """
        question_lower = question.lower()
        
        # Pattern untuk pertanyaan simple yang bisa dijawab langsung
        
        # Nama sekolah
        if "nama sekolah" in question_lower or "nama smk" in question_lower:
            nama = self.data.get("profile", {}).get("nama", None)
            if nama:
                return f"{nama} adalah sekolah menengah kejuruan yang berlokasi di Bojonegoro."
        
        # Alamat
        if "alamat" in question_lower or "di mana" in question_lower or "dimana" in question_lower:
            alamat = self.data.get("profile", {}).get("alamat", None)
            if alamat:
                return f"SMKN 4 Bojonegoro berlokasi di {alamat}. Sekolah ini mudah diakses dan berada di lokasi strategis."
        
        # Kepala sekolah
        if "kepala sekolah" in question_lower or "kepsek" in question_lower:
            kepsek = self.data.get("profile", {}).get("kepala_sekolah", None)
            if kepsek:
                return f"Kepala Sekolah SMKN 4 Bojonegoro saat ini adalah {kepsek}."
        
        # Jumlah siswa
        if "berapa siswa" in question_lower or "jumlah siswa" in question_lower:
            siswa = self.data.get("profile", {}).get("jumlah_siswa", None)
            if siswa:
                return f"SMKN 4 Bojonegoro memiliki {siswa} siswa yang tersebar di berbagai jurusan."
        
        # Jumlah guru
        if "berapa guru" in question_lower or "jumlah guru" in question_lower:
            guru = self.data.get("profile", {}).get("jumlah_guru", None)
            if guru:
                return f"Sekolah ini memiliki {guru} guru profesional yang siap membimbing siswa."
        
        # List jurusan - lebih detail
        if ("jurusan apa" in question_lower or "ada jurusan" in question_lower or 
            "jurusan yang tersedia" in question_lower or "jurusan di" in question_lower):
            jurusan_data = self.data.get("jurusan", {})
            if jurusan_data:
                jurusan_list = list(jurusan_data.keys())
                return f"SMKN 4 Bojonegoro memiliki {len(jurusan_list)} jurusan unggulan: {', '.join(jurusan_list)}. Semua jurusan dirancang untuk mempersiapkan siswa memasuki dunia kerja atau melanjutkan kuliah."
        
        # Akreditasi
        if "akreditasi" in question_lower:
            akred = self.data.get("profile", {}).get("akreditasi", None)
            if akred:
                return f"SMKN 4 Bojonegoro berakreditasi {akred}, yang menunjukkan kualitas pendidikan yang baik dan terstandar."
        
        # Visi
        if "visi" in question_lower and "misi" not in question_lower:
            visi = self.data.get("profile", {}).get("visi", None)
            if visi:
                return f"Visi SMKN 4 Bojonegoro: {visi}"
        
        # Tambahan: Pertanyaan umum tentang jurusan tanpa data spesifik
        if "apa itu rpl" in question_lower or "rpl itu apa" in question_lower:
            return None  # Biarkan LLM jelaskan dengan lebih baik
        
        if "apa itu tkj" in question_lower or "tkj itu apa" in question_lower:
            return None  # Biarkan LLM jelaskan dengan lebih baik
        
        if "apa itu mm" in question_lower or "multimedia itu apa" in question_lower:
            return None  # Biarkan LLM jelaskan dengan lebih baik
        
        return None

# Global retrieval service instance
retrieval_service = RetrievalService()
