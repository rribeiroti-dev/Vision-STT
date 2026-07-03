# Computer Vision & Speech to Text Production Platform

Aplicações Web nativa desenvolvida em Python de alto desempenho para ingestão de imagens de câmeras em tempo real, pipeline de análise determinística computacional estruturada utilizando OpenCV e transcrição automática de áudio com Faster-Whisper. Todos os dados são consolidados em banco relacional escalável Neon.tech.

## 🚀 Tecnologias Empregadas
* **Front-End / Interface:** Streamlit (Layout Responsivo por Abas)
* **Visão Computacional:** OpenCV, Pillow, NumPy
* **Speech-to-Text:** Faster-Whisper (Modelo Tiny otimizado para CPU)
* **Persistência de Dados:** PostgreSQL (Provedor Serverless Neon.tech)
* **ORM e Conexões:** SQLAlchemy, Psycopg 3
* **Hospedagem & Nuvem:** Render Engine Platform

## 📐 Padrões Arquiteturais e Boas Práticas
* **Clean Architecture:** Separação estrita em camadas: Configuração, Modelos, Repositórios, Serviços, Controladores e Views.
* **Princípios SOLID:** Baixíssimo acoplamento entre a interface do Streamlit e as regras estruturais de visão computacional.
* **Injeção de Dependências:** O gerenciamento de sessões do banco de dados é tratado através de geradores reutilizáveis nativos.
---

## 🚀 Funcionalidades Principais

* **📸 Captura e Análise de Imagem:** Integração nativa com a webcam para capturar fotos, processando métricas de luminosidade, grau de nitidez, paleta de cores média (RGB) e detecção de rostos via Classificadores Haar Cascade.
* **🎤 Transcrição de Áudio em PT-BR (100% Gratuita):** Captura de observações por voz diretamente do microfone com processamento e transcrição nativa em Português do Brasil usando a API pública do Google (*SpeechRecognition*), sem custos ou chaves de API.
* **🔥 Fluxo Unificado Inteligente:** Captura de imagem e gravação de áudio feitas de forma sequencial na interface, acionando ambos os pipelines com um único clique operacional.
* **💾 Banco de Dados Híbrido:** Suporte automático e transparente para **SQLite** (ambiente de desenvolvimento local) e **PostgreSQL / Neon.tech** (ambiente de produção na nuvem).
* **📊 Histórico Dinâmico:** Visualização completa e filtrada de registros passados, com gráficos de métricas e exibição de imagens salvas.

---

## 🛠️ Arquitetura de Pastas do Projeto

O ecossistema segue o padrão arquitetural MVC adaptado para microsserviços em engenharia de dados:

```text
📂 computer-vision-streamlit/
├── 📂 assets/              # Armazenamento local de mídias (fotos salvas)
│   └── 📂 images/
├── 📂 config/              # Centralização de configurações globais do app
│   └── settings.py
├── 📂 controllers/         # Orquestração de fluxo entre views e serviços
│   └── main_controller.py
├── 📂 database/            # Conexão, sessão e ciclo de vida do SQLAlchemy
│   └── connection.py
├── 📂 models/              # Mapeamento ORM/Tabelas relacionais
│   └── analise.py
├── 📂 repositories/        # Camada de abstração e consultas ao banco (CRUD)
│   └── analise_repository.py
├── 📂 services/            # Lógica pura de visão computacional e áudio
│   ├── cv_service.py
│   └── stt_service.py
├── 📂 utils/               # Inicializadores de banco e utilitários
│   └── db_init.py
├── .env                    # Variáveis de ambiente locais (Ignorado pelo Git)
├── .env.example            # Modelo de configuração para novos ambientes
├── .gitignore              # Proteção de credenciais e cache
├── app.py                  # Ponto de entrada (Interface Visual Streamlit)
└── requirements.txt        # Gerenciamento de dependências otimizado
---

## 🛠️ Instalação e Execução Local

O projeto foi inteiramente preparado para rodar diretamente na sua máquina de forma simples, **sem necessidade de ambientes virtuais complexos (venv)**.

### 1. Instalação das Dependências
Abra seu terminal diretamente na pasta raiz do projeto e execute:
```bash
pip install -r requirements.txt
```

### 2. Configurações Globais (.env)
Duplique o arquivo `.env.example` e renomeie-o para `.env`. Preencha com suas credenciais do banco Neon.tech:
```env
DATABASE_URL=postgresql+psycopg://usuario:senha@ep-nome-banco.us-east-1.aws.neon.tech/dbname?sslmode=require
UPLOAD_FOLDER=assets/images
PYTHON_VERSION=3.12.8

```

### 3. Inicialização da Aplicação
Com o banco conectado, dispare o comando:
```bash
streamlit run app.py
```

---

## ☁️ Instruções para Deploy Automatizado no Render

A arquitetura está otimizada para integração contínua (CI/CD) via GitHub conectada ao **Render**:

1. Crie um novo repositório no **GitHub** e envie os arquivos deste projeto.
2. Acesse sua conta no painel do Render.
3. Clique em **New +** e selecione **Web Service**.
4. Conecte o repositório GitHub correspondente ao projeto.
5. No formulário de criação, configure exatamente os parâmetros abaixo:
   * **Runtime:** `Python`
   * **Build Command:** `pip install -r requirements.txt`
   * **Start Command:** `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
6. Abra a seção **Advanced -> Environment Variables** e cadastre as variáveis contidas no `.env`:
   * `DATABASE_URL` = *(Sua string de conexão segura fornecida pelo painel do Neon.tech)*
   * `UPLOAD_FOLDER` = `assets/images`
7. Conclua clicando em **Create Web Service**. O deploy ocorrerá de forma 100% automatizada a cada novo `git push` efetuado na branch principal.
