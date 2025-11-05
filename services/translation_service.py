from deep_translator import GoogleTranslator
from typing import Optional

class TranslationService:
    def __init__(self):
        pass
        
    async def translate_text(self, text: str, target_language: str, source_language: Optional[str] = None) -> str:
        """
        Translate text to target language.
        
        Args:
            text: Text to translate
            target_language: Target language code ('en' or 'ja')
            source_language: Source language code (auto-detected if None)
        """
        try:
            # Map our language codes to Google Translate codes
            lang_mapping = {
                'en': 'en',
                'ja': 'ja'
            }
            
            target_lang = lang_mapping.get(target_language, 'en')
            source_lang = lang_mapping.get(source_language, 'auto') if source_language else 'auto'
            
            translator = GoogleTranslator(source=source_lang, target=target_lang)
            result = translator.translate(text)
            
            return result
            
        except Exception as e:
            # Fallback: return original text if translation fails
            print(f"Translation failed: {e}")
            return text
            
    def detect_language(self, text: str) -> str:
        """
        Detect the language of the given text using langdetect.
        """
        try:
            from langdetect import detect
            detected_lang = detect(text)
            
            # Map to our supported languages
            if detected_lang in ['ja', 'jp']:
                return 'ja'
            else:
                return 'en'
                
        except Exception as e:
            print(f"Language detection failed: {e}")
            return 'en'  # Default to English