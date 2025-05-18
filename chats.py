from google.genai import types
from google import genai

class CorretorChat:
    def __init__(self, gabarito):
        client = genai.Client()
        chat_config = types.GenerateContentConfig(
            system_instruction = """
                    Voce se comportará como um professor de quimica, explicando de forma clara e concisa conceitos sobre o assunto. 
                    Focado em alunos do ensino mpedio
                """,
        )

        self.chat = client.chats.create(model="gemini-2.0-flash", config=chat_config)
        conteudo_inicial = ["""Considere a seguinte imagem como gabarito de uma questão apresentada aos alunos. Usará ela para corrigir futuras questões a partir de imagens enviadas""", gabarito]

        self.chat.send_message(conteudo_inicial)

    def corrigir_questao(self, img, aluno):
        cont = ["Corrija a questão contida na imagem, feita pelo aluno"+aluno+", informando se a resposta está correta ou não, e retornando uma breve explicação em caso de erro.", img]
        return self.chat.send_message(cont)
        
    def get_summary(self):
        return self.chat.send_message("""
            Retorne o histórico das correções feitas até agora
            estruture de forma que fique claro qual aluno fez qual questão e qual foi o feedback dado por você.
        """).text
