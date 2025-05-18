import os
import warnings
from IPython.display import HTML, Markdown
from agents import Corretor, Analisador
from img_helper import load_png
from chats import CorretorChat
from PIL import Image

warnings.filterwarnings("ignore")

os.environ["GOOGLE_API_KEY"] = "Insira_sua_chave_aqui"

corretor = Corretor()

image = Image.open('imgs/q1.gabarito.jpeg')

corretor = CorretorChat(image)

resp = corretor.corrigir_questao(Image.open('imgs/q1.resposta 1.jpeg'), "aluno 1")
print("-----")
print(resp.text)

resp = corretor.corrigir_questao(Image.open('imgs/q1.resposta 2.jpeg'), "aluno 2")
print("-----")
print(resp.text)


resp = corretor.corrigir_questao(Image.open('imgs/q1.resposta 3.jpeg'), "aluno 3")
print("-----")
print(resp.text)

print("-----")

print(corretor.get_summary())

feedbackGenerator = Analisador()
resp = feedbackGenerator.gerar_feedback(corretor.get_summary())
print(resp)
