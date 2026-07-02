from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from config.settings import DATABASE_URL, logger

if not DATABASE_URL:
    logger.error("DATABASE_URL não configurada nas variáveis de ambiente.")
    raise ValueError("DATABASE_URL não informada.")

# Configuração Híbrida Inteligente
if DATABASE_URL.startswith("sqlite"):
    # Configuração específica e leve para o SQLite Local
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    # Configuração robusta para o PostgreSQL/Neon em produção
    engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_size=5, max_overflow=10)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Context manager para fornecer sessões do banco de dados de forma segura."""
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Erro na sessão de banco de dados: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()