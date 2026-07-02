from sqlalchemy.orm import Session
from models.analise import AnaliseModel
from typing import List, Optional
from datetime import datetime
from config.settings import logger

class AnaliseRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, analise: AnaliseModel) -> AnaliseModel:
        try:
            self.db.add(analise)
            self.db.commit()
            self.db.refresh(analise)
            return analise
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro ao salvar análise no banco: {str(e)}")
            raise e

    def find_all(self, search: Optional[str] = None, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[AnaliseModel]:
        try:
            query = self.db.query(AnaliseModel)
            if search:
                query = query.filter(
                    (AnaliseModel.descricao.ilike(f"%{search}%")) |
                    (AnaliseModel.objetos.ilike(f"%{search}%")) |
                    (AnaliseModel.transcricao.ilike(f"%{search}%"))
                )
            if start_date:
                query = query.filter(AnaliseModel.created_at >= start_date)
            if end_date:
                query = query.filter(AnaliseModel.created_at <= end_date)
            
            return query.order_by(AnaliseModel.created_at.desc()).all()
        except Exception as e:
            logger.error(f"Erro ao buscar análises: {str(e)}")
            return []

    def delete_by_id(self, analise_id: int) -> bool:
        try:
            analise = self.db.query(AnaliseModel).filter(AnaliseModel.id == analise_id).first()
            if analise:
                self.db.delete(analise)
                self.db.commit()
                return True
            return False
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro ao excluir análise {analise_id}: {str(e)}")
            return False

    def update_transcricao(self, analise_id: int, transcricao: str) -> bool:
        try:
            analise = self.db.query(AnaliseModel).filter(AnaliseModel.id == analise_id).first()
            if analise:
                analise.transcricao = transcricao
                self.db.commit()
                return True
            return False
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro ao atualizar transcrição {analise_id}: {str(e)}")
            return False
