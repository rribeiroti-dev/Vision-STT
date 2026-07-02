import streamlit as st

# Configuração da página Streamlit deve ser o PRIMEIRO comando executado
st.set_page_config(
    page_title="Vision-STT Production Platform",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

from utils.db_init import inicializar_banco_de_dados
from controllers.main_controller import MainController
from database.connection import get_db
from repositories.analise_repository import AnaliseRepository
from audio_recorder_streamlit import audio_recorder     # <--- LINHA CORRIGIDA
from PIL import Image
import os
from datetime import datetime

# Inicializar Tabelas Dinamicamente
inicializar_banco_de_dados()

controller = MainController()

# --- INTERFACE STRUCTURING ---
st.title("🧠 Vision-STT Production Platform")
st.markdown("---")

# Menu Lateral (Sidebar)
with st.sidebar:
    st.header("⚡ Sistema & Conectividade")
    st.success("Conectado ao Neon.tech (PostgreSQL)")
    st.info("Hospedagem activa via Render")
    
    st.markdown("---")
    st.markdown("### 📊 Menu de Navegação")
    st.markdown("- **Painel de Captura Principal**")
    st.markdown("Consulte as abas superiores para acessar o Histórico Avançado e o Dashboard Analítico.")

# Layout de Abas para Organização Visual Limpa
tab_captura, tab_historico, tab_dashboard = st.tabs(["📸 Captura e Processamento", "🗂️ Histórico Base", "📈 Dashboard e Métricas"])

with tab_captura:
    col_input, col_output = st.columns(2)

    with col_input:
        st.subheader("📡 Entrada de Dispositivos")
        
        # 1. Seção da Câmera
        st.markdown("### 📸 Captura de Imagem")
        camera_file = st.camera_input("Alinhar webcam para captura")
        
        st.markdown("---")
        
        # 2. Seção do Microfone (Totalmente Separada)
        st.markdown("### 🎤 Observações em Áudio (Speech to Text)")
        audio_recorded = audio_recorder()
        
        if audio_recorded:
            st.audio(audio_recorded, format="audio/wav")
            # Botão exclusivo para processar APENAS o áudio se o usuário quiser
            if st.button("🗣️ Transcrever Apenas Áudio", use_container_width=True):
                with st.spinner("Transcrevendo áudio..."):
                    texto_transcrito = controller.stt_service.transcrever(audio_recorded)
                    st.info(f"✨ **Resultado da Transcrição:** {texto_transcrito}")

    with col_output:
        st.subheader("🖥️ Resultados e Ações")
        
        # Se houver imagem capturada, mostra o preview na direita
        if camera_file is not None:
            st.image(camera_file, caption="Frame Capturado", use_container_width=True)
            
            # Botão principal que processa a imagem (e junta o áudio se ele existir)
            if st.button("🔥 Executar Análise Completa (Imagem + Áudio)", use_container_width=True):
                with st.spinner("Executando pipelines de processamento interno..."):
                    try:
                        img_bytes = camera_file.getvalue()
                        aud_bytes = audio_recorded if audio_recorded else None
                        
                        resultado = controller.processar_fluxo_completo(img_bytes, aud_bytes)
                        
                        st.success("🎉 Processamento Concluído e Persistido!")
                        
                        # Exibição das Métricas Visuais
                        st.markdown(f"### 📊 Resultados do ID #{resultado.id}")
                        st.write(f"**Descrição:** {resultado.descricao}")
                        st.write(f"**Objetos Encontrados:** {resultado.objetos}")
                        st.write(f"**Rostos Detectados:** {resultado.rostos}")
                        st.write(f"**Métricas de Luminosidade:** {resultado.luminosidade}")
                        st.write(f"**Grau de Nitidez:** {resultado.nitidez}")
                        st.write(f"**Paleta de Cores (RGB Médio):** {resultado.cores}")
                        
                        if resultado.transcricao:
                            st.info(f"🗣️ **Transcrição Vinculada:** {resultado.transcricao}")
                            
                    except Exception as e:
                        st.error(f"Falha operacional no processamento: {str(e)}")
        else:
            st.info("Aguardando captura ativa de imagem pela webcam para habilitar análise visual.")

with tab_historico:
    st.subheader("🗂️ Repositório e Histórico das Análises")
    
    db_session = next(get_db())
    repo = AnaliseRepository(db_session)
    
    # Filtros Avançados
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        search_term = st.text_input("🔍 Buscar por conteúdo (Texto, Objetos, Transcrição)")
    with col_f2:
        d_inicio = st.date_input("Data Inicial", value=None)
    with col_f3:
        d_fim = st.date_input("Data Final", value=None)
        
    dt_inicio = datetime.combine(d_inicio, datetime.min.time()) if d_inicio else None
    dt_fim = datetime.combine(d_fim, datetime.max.time()) if d_fim else None

    # Consulta dos Dados filtrados
    registros = repo.find_all(search=search_term, start_date=dt_inicio, end_date=dt_fim)
    
    if registros:
        import pandas as pd
        import json
        
        # Exportações Globais do Dataset Filtrado
        dados_export = [{
            "id": r.id, "created_at": str(r.created_at), "descricao": r.descricao,
            "objetos": r.objetos, "pessoas": r.quantidade_pessoas, "transcricao": r.transcricao
        } for r in registros]
        
        df_export = pd.DataFrame(dados_export)
        
        col_exp1, col_exp2 = st.columns(2)
        with col_exp1:
            st.download_button("📥 Exportar Filtro para CSV", df_export.to_csv(index=False), "export.csv", "text/csv")
        with col_exp2:
            st.download_button("📥 Exportar Filtro para JSON", json.dumps(dados_export, indent=2), "export.json", "application/json")
        
        st.markdown("---")
        
        # Lista Grid de Cards do Histórico
        for reg in registros:
            with st.container():
                c_img, c_det = st.columns([1, 2])
                with c_img:
                    if os.path.exists(reg.image_path):
                        st.image(Image.open(reg.image_path), use_container_width=True)
                        with open(reg.image_path, "rb") as file_img:
                            st.download_button(f"💾 Download Image #{reg.id}", file_img, f"img_{reg.id}.jpg", "image/jpeg")
                    else:
                        st.error("Arquivo de imagem ausente no servidor.")
                with c_det:
                    st.markdown(f"#### Registro #{reg.id} — {reg.created_at.strftime('%d/%m/%Y %H:%M:%S')}")
                    st.write(f"**Descrição:** {reg.descricao}")
                    st.write(f"**Objetos:** {reg.objetos} | **Pessoas:** {reg.quantidade_pessoas}")
                    st.write(f"**Luminosidade:** {reg.luminosidade} | **Nitidez:** {reg.nitidez}")
                    if reg.transcricao:
                        st.info(f"🗣️ **Transcrição:** {reg.transcricao}")
                        
                    # Gerenciamento de Áudio e Exclusões individuais
                    col_b1, col_b2 = st.columns(2)
                    with col_b1:
                        if st.button(f"❌ Excluir Registro #{reg.id}", key=f"del_{reg.id}"):
                            if repo.delete_by_id(reg.id):
                                st.success("Registro removido com sucesso do banco.")
                                st.rerun()
                    with col_b2:
                        if reg.transcricao and st.button(f"🤫 Remover Texto de Áudio #{reg.id}", key=f"del_aud_{reg.id}"):
                            if repo.update_transcricao(reg.id, ""):
                                st.success("Transcrição limpa.")
                                st.rerun()
                st.markdown("---")
    else:
        st.info("Nenhum registro localizado para os filtros informados.")

with tab_dashboard:
    st.subheader("📈 Painel Executivo e Analytics")
    
    db_session = next(get_db())
    repo_dash = AnaliseRepository(db_session)
    todos = repo_dash.find_all()
    
    if todos:
        import pandas as pd
        df = pd.DataFrame([{
            "id": t.id,
            "pessoas": t.quantidade_pessoas,
            "data": t.created_at.date()
        } for t in todos])
        
        m_totais, m_pessoas = st.columns(2)
        with m_totais:
            st.metric(label="Total de Análises Executadas", value=len(df))
        with m_pessoas:
            st.metric(label="Total de Rostos Identificados", value=int(df["pessoas"].sum()))
            
        st.markdown("#### Volume Operacional Diário")
        chart_data = df.groupby("data").size().reset_index(name="Quantidade de Capturas")
        st.line_chart(chart_data.set_index("data"))
    else:
        st.info("Dados analíticos indisponíveis devido à ausência de registros no banco.")
