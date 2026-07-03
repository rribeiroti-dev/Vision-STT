import os
import io
import tempfile
from config.settings import logger

class SpeechToTextService:
    def __init__(self):
        self.recognizer = None

    def _lazy_init(self):
        if self.recognizer is None:
            import speech_recognition as sr
            self.recognizer = sr.Recognizer()

    def transcrever(self, audio_bytes: bytes) -> str:
        try:
            if not audio_bytes or len(audio_bytes) < 100:
                return "Áudio inválido ou muito curto."

            self._lazy_init()
            import speech_recognition as sr

            # Salva os bytes em um arquivo temporário no formato WAV exigido pela biblioteca
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
                temp_audio.write(audio_bytes)
                temp_path = temp_audio.name

            try:
                with sr.AudioFile(temp_path) as source:
                    # Ajusta ruídos de fundo automaticamente
                    self.recognizer.adjust_for_ambient_noise(source)
                    audio_data = self.recognizer.record(source)
                    
                # Executa a transcrição gratuita usando a API pública do Google em PT-BR
                transcricao = self.recognizer.recognize_google(audio_data, language="pt-BR")
                return transcricao
                
            except sr.UnknownValueError:
                return "O motor de transcrição gratuita não conseguiu compreender a fala."
            except sr.RequestError as e:
                return f"Falha de comunicação com o serviço gratuito de transcrição: {str(e)}"
            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)

        except Exception as e:
            logger.error(f"Erro no pipeline de Speech-to-Text gratuito: {str(e)}")
            return f"Falha interna na transcrição: {str(e)}"
