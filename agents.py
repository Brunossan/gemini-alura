from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search
from google.genai import types  # Para criar conteúdos (Content e Part)

# def load_png_as_part(path: str) -> types.Part:
#     with open(path, "rb") as f:
#     png_bytes = f.read()
#     display(Image(path))
#     return types.Part(inline_data=types.Blob(mime_type="image/png", data=png_bytes))

def call_agent(agent: Agent, message_text: str, image_data: bytes = None) -> str:
    # Cria um serviço de sessão em memória
    session_service = InMemorySessionService()
    # Cria uma nova sessão (você pode personalizar os IDs conforme necessário)
    session = session_service.create_session(app_name=agent.name, user_id="user1", session_id="session1")
    # Cria um Runner para o agente
    runner = Runner(agent=agent, app_name=agent.name, session_service=session_service)

    parts = [types.Part(text=message_text)]
    if image_data:
        parts.append(types.Part(inline_data=types.Blob(mime_type="image/jpeg", data=image_data))) # Assuming JPEG format
        # parts.append(types.Part(mime_type="image/jpeg", data=image_data)) # Assuming JPEG format

    # Cria o conteúdo da mensagem de entrada
    content = types.Content(role="user", parts=parts)
    
    final_response = ""
    # Itera assincronamente pelos eventos retornados durante a execução do agente
    for event in runner.run(user_id="user1", session_id="session1", new_message=content):
        if event.is_final_response():
          for part in event.content.parts:
            if part.text is not None:
              final_response += part.text
              final_response += "\n"
    return final_response

class Corretor:
    def __init__(self):
        self.agnt = Agent(
            name="corretor",
            model="gemini-2.0-flash",
            instruction="""
                Voce se comportará como um professor de quimica, explicando de forma clara e concisa conceitos sobre o assunto. 
                Seu objetivo é ajudar os alunos do ensino médio a entenderem melhor os conceitos de química,
                respondendo perguntas e fornecendo explicações breves.
            """,
            description = "Agente revior de exercicios de quimica"
        )

    def perguntar(self, prompt):
        resposta = call_agent(self.agnt, prompt)
        return resposta
        
    def corrigir(self, imagem):
        resposta = call_agent(self.agnt, "Corrija a questão contida na imagem, informando se a resposta está correta ou não, e retornando uma breve explicação em caso de erro.", imagem)
        return resposta

    #Non funciona: deveria ser um chat com histórico e não um agente pra poder fazer isso :(
    # nem faz sentido isso ser um obj.. tlvz :)
    def definir_gabarito(self, imagem):
        resposta = call_agent(self.agnt, """
            Considere a seguinte imagem como gabarito de uma questão apresentada aos alunos. 
            Voce usará como base para corrigir futuras questões a partir de imagens enviadas
        """, imagem)
        return resposta

class Analisador:
    def __init__(self):
        self.agnt = Agent(
            name="Analisador",
            model="gemini-2.0-flash",
            instruction="""
                Sua função é gerar insights e feedbacks para professores de quimica dado uma lista com a correção de uma questão para diferentes alunos.
                Esta analise deve conter quantos alunos acertaram, quantos erraram e quais foram os erros mais comuns.
                Além disso, você deve fornecer uma sugestão para o professor sobre como melhorar o ensino do assunto para este grupo. 
            """,
            description = "Agente gerador de feedback para professores de quimica"
        )

    def gerar_feedback(self, resps):
        resposta = call_agent(self.agnt, resps)
        return resposta

