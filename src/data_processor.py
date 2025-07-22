"""
Procesador de datos para UltraEfficientLLM
"""

import requests
import os
import re
from typing import List, Optional


class DataProcessor:
    """Procesador de datos para descargar y limpiar textos de libros"""
    
    def __init__(self):
        self.downloaded_books = {}
    
    def download_book(self, url: str, filename: str = None) -> str:
        """
        Descarga un libro desde Project Gutenberg
        
        Args:
            url: URL del libro en Project Gutenberg
            filename: Nombre del archivo local (opcional)
            
        Returns:
            str: Contenido del libro descargado
        """
        if filename is None:
            filename = f'downloaded_book_{len(self.downloaded_books)}.txt'
        
        print(f"📥 Descargando libro desde: {url}")
        
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            # Guardar archivo
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"✅ Libro descargado exitosamente: {filename}")
            
            # Leer y procesar contenido
            content = self.read_and_clean_book(filename)
            self.downloaded_books[filename] = content
            
            return content
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error descargando el libro: {e}")
            raise
    
    def read_and_clean_book(self, filename: str) -> str:
        """
        Lee y limpia un archivo de libro
        
        Args:
            filename: Ruta del archivo
            
        Returns:
            str: Contenido limpio del libro
        """
        print(f"📖 Leyendo y limpiando: {filename}")
        
        try:
            # Intentar con UTF-8
            with open(filename, 'r', encoding='utf-8') as f:
                raw_content = f.read()
                print(f"✅ Archivo leído con UTF-8")
                
        except UnicodeDecodeError:
            print("⚠️ UTF-8 falló, intentando con Latin-1")
            try:
                with open(filename, 'r', encoding='latin-1') as f:
                    raw_content = f.read()
                    print(f"✅ Archivo leído con Latin-1")
            except Exception as e:
                print(f"❌ Error leyendo archivo: {e}")
                raise
        
        # Limpiar contenido
        cleaned_content = self._clean_gutenberg_content(raw_content)
        
        print(f"📊 Contenido procesado: {len(cleaned_content)} caracteres")
        return cleaned_content
    
    def _clean_gutenberg_content(self, raw_content: str) -> str:
        """
        Limpia contenido de Project Gutenberg
        
        Args:
            raw_content: Contenido crudo del archivo
            
        Returns:
            str: Contenido limpio
        """
        # Marcadores de Project Gutenberg
        start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK"
        end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK"
        
        start_index = raw_content.find(start_marker)
        end_index = raw_content.find(end_marker)
        
        if start_index != -1 and end_index != -1:
            # Extraer contenido entre marcadores
            book_content = raw_content[start_index + len(start_marker):end_index]
            print("✅ Headers y footers de Project Gutenberg removidos")
        else:
            print("⚠️ No se encontraron marcadores de Project Gutenberg, usando contenido completo")
            book_content = raw_content
        
        # Convertir a minúsculas
        book_content = book_content.lower()
        print("✅ Texto convertido a minúsculas")
        
        return book_content
    
    def split_into_chunks(self, text: str, chunk_size: int = 1000) -> List[str]:
        """
        Divide el texto en chunks para entrenamiento
        
        Args:
            text: Texto a dividir
            chunk_size: Tamaño de cada chunk
            
        Returns:
            List[str]: Lista de chunks
        """
        chunks = []
        words = text.split()
        
        for i in range(0, len(words), chunk_size):
            chunk = " ".join(words[i:i + chunk_size])
            if chunk.strip():
                chunks.append(chunk)
        
        print(f"📝 Texto dividido en {len(chunks)} chunks")
        return chunks
    
    def get_sample_texts(self) -> List[str]:
        """
        Retorna textos de ejemplo para testing
        
        Returns:
            List[str]: Lista de textos de ejemplo
        """
        return [
            "The quick brown fox jumps over the lazy dog.",
            "Machine learning is a subset of artificial intelligence.",
            "Natural language processing enables computers to understand human language.",
            "Deep learning uses neural networks with multiple layers.",
            "The future of AI depends on efficient algorithms and powerful hardware."
        ]
    
    def save_processed_data(self, content: str, filename: str) -> None:
        """
        Guarda datos procesados
        
        Args:
            content: Contenido a guardar
            filename: Nombre del archivo
        """
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"💾 Datos guardados en: {filename}")
    
    def load_processed_data(self, filename: str) -> str:
        """
        Carga datos procesados
        
        Args:
            filename: Nombre del archivo
            
        Returns:
            str: Contenido cargado
        """
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"📂 Datos cargados desde: {filename}")
        return content 