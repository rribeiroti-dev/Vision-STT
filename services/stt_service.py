import os
import tempfile
from config.settings import logger

class SpeechToTextService:
    def __init__(self):
        self.client = None

    def _lazy_init(self):
        if self.client is None:
            from openai import OpenAI
            api_key = os.getenv("OPENAI_API_KEY", "mock-key-caso-nao-configurado")
            base_url = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
            self.client = OpenAI(api_key=api_key, base_url=base_url)

    def transcrever(self, audio_bytes: bytes) -> str:
        try:
            if not audio_bytes or len(audio_bytes) < 100:
                return "Áudio inválido ou muito curto."

            # Modo de Simulação Inteligente para testes locais rápidos
            if not os.getenv("OPENAI_API_KEY"):
                return "[Modo de Simulação] Áudio capturado com sucesso! Para transcrição real, insira a OPENAI_API_KEY no arquivo .env."

            self._lazy_init()
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
                temp_audio.write(audio_bytes)
                temp_path = temp_audio.name

            try:
                with open(temp_path, "rb") as audio_file:
                    transcript = self.client.audio.transcriptions.create(
                        model="whisper-1", 
                        file=audio_file
                    )
                return transcript.text
            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)

        except Exception as e:
            logger.error(f"Erro no pipeline de Speech-to-Text via API: {str(e)}")
            return f"Falha na transcrição de áudio: {str(e)}"