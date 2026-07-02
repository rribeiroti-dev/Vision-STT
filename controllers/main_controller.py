import uuid
from pathlib import Path
from config.settings import UPLOAD_FOLDER, logger
from database.connection import get_db
from models.analise import AnaliseModel
from repositories.analise_repository import AnaliseRepository
from services.cv_service import ComputerVisionService
from services.stt_service import SpeechToTextService
from datetime import datetime

class MainController:
    def __init__(self):
        self.cv_service = ComputerVisionService()
        self.stt_service = SpeechToTextService()

    def processar_fluxo_completo(self, image_bytes: bytes, audio_bytes: bytes = None) -> AnaliseModel:
        db_context = next(get_db())
        repository = AnaliseRepository(db_context)
        
        try:
            # 1. Pipeline de Visão Computacional
            metrics = self.cv_service.analisar_imagem(image_bytes)

            # 2. Pipeline de Speech-to-Text (Se houver áudio)
            transcricao_texto = ""
            if audio_bytes is not None:
                # A nova biblioteca injeta os bytes diretamente
                transcricao_texto = self.stt_service.transcrever(audio_bytes)

            # 3. Salvar Imagem em Disco
            filename = f"cap_{uuid.uuid4().hex}.jpg"
            full_path = UPLOAD_FOLDER / filename
            with open(full_path, "wb") as f:
                f.write(image_bytes)

            # 4. Construção da Entidade do Modelo Relacional
            analise_model = AnaliseModel(
                image_path=str(full_path),
                descricao=metrics["descricao"],
                objetos=metrics["objetos"],
                quantidade_pessoas=metrics["quantidade_pessoas"],
                rostos=metrics["rostos"],
                idade=metrics["idade"],
                emocao=metrics["emocao"],
                cores=metrics["cores"],
                luminosidade=metrics["luminosidade"],
                nitidez=metrics["nitidez"],
                transcricao=transcricao_texto,
                json_resultado=metrics
            )

            # 5. Persistência de Dados
            saved_entity = repository.save(analise_model)
            logger.info(f"Análise processada e salva com ID: {saved_entity.id}")
            return saved_entity

        except Exception as e:
            logger.error(f"Erro crítico no fluxo controlado da aplicação: {str(e)}")
            raise e
