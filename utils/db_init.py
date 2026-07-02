from database.connection import Base, engine
from models.analise import AnaliseModel
from config.settings import logger

def inicializar_banco_de_dados():
    """Garante a criação automática de tabelas se elas não existirem no Neon.tech."""
    try:
        logger.info("Verificando/Criando tabelas relacionais...")
        Base.metadata.create_all(bind=engine)
        logger.info("Tabelas estruturadas com sucesso.")
    except Exception as e:
        logger.critical(f"Erro crítico na inicialização das tabelas: {str(e)}")
