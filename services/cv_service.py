import cv2
import numpy as np
from PIL import Image
from datetime import datetime
from config.settings import logger

class ComputerVisionService:
    def __init__(self):
        # Carrega classificadores pré-treinados do OpenCV (Haar Cascades)
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def analisar_imagem(self, image_bytes: bytes) -> dict:
        """Executa pipeline determinística estruturada de visão computacional."""
        try:
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if img is None:
                raise ValueError("Incapaz de decodificar os bytes da imagem.")

            height, width, _ = img.shape
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # 1. Detecção de Rostos e estimativa simples de metadados associados
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            num_faces = len(faces)

            # 2. Luminosidade (Brilho Médio)
            brilho_medio = np.mean(gray)
            luminosidade_label = "Boa" if 80 <= brilho_medio <= 200 else ("Baixa (Escuro)" if brilho_medio < 80 else "Alta (Exposto)")

            # 3. Nitidez (Variância do Laplaciano)
            nitidez_val = cv2.Laplacian(gray, cv2.CV_64F).var()
            nitidez_label = "Nítida" if nitidez_val > 100 else "Desfocada/Suave"

            # 4. Análise de Cores Predominantes (K-Means simplificado via histograma)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            hist_r = np.mean(img_rgb[:, :, 0])
            hist_g = np.mean(img_rgb[:, :, 1])
            hist_b = np.mean(img_rgb[:, :, 2])
            
            cores_predominantes = f"R:{int(hist_r)} G:{int(hist_g)} B:{int(hist_b)}"

            # 5. Mapeamento heurístico de objetos gerais
            objetos_detectados = ["Estrutura de Background"]
            if num_faces > 0:
                objetos_detectados.append("Silhueta Humana")

            now = datetime.now()

            return {
                "descricao": f"Captura estática em ambiente com luminosidade {luminosidade_label.lower()}.",
                "objetos": ", ".join(objetos_detectados),
                "quantidade_pessoas": num_faces,
                "rostos": num_faces,
                "idade": "Não disponível (Requer IA Proprietária)",
                "emocao": "Não disponível (Requer IA Proprietária)",
                "cores": cores_predominantes,
                "luminosidade": f"{luminosidade_label} ({int(brilho_medio)})",
                "nitidez": f"{nitidez_label} ({int(nitidez_val)})",
                "resolucao": f"{width}x{height}",
                "data": now.strftime("%Y-%m-%d"),
                "horario": now.strftime("%H:%M:%S")
            }
        except Exception as e:
            logger.error(f"Erro no pipeline de visão computacional: {str(e)}")
            raise e
