from flet import *



#conectando ao db
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("./service_account.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

''' para editar um arquivo....doc_ref = db.collection("users").document("agendamentos")
            doc_ref.set({"nome": f"{nomeCliente.value}", "dia": dia, "hora": hora})'''

def main(pagina:Page):
    pagina.vertical_alignment = MainAxisAlignment.SPACE_AROUND

    domingos = (3, 10, 17, 24)

    # adicionar dados a lista
    clientesAgendados = []
    datasAgendadas = []

        


    

    # retornar a pagina principal

    def returnPage(e):
        dataCliente.value = dataCliente.value
        horarioCliente.value = horarioCliente.value
        senhainput.value = ''
        pagina.clean()
        pagina.add(
            Row([Text("AGENDE SEU CORTE NO MÊS DE DEZEMBRO !")],
                    alignment=MainAxisAlignment.CENTER),
            Row([nomeCliente], alignment=MainAxisAlignment.CENTER),
            Row([dataCliente], alignment=MainAxisAlignment.CENTER),
            Row([horarioCliente], alignment=MainAxisAlignment.CENTER),
            Row([botao], alignment=MainAxisAlignment.CENTER),
            #Row([botao_cadastros], alignment=MainAxisAlignment.CENTER),
        )
        pagina.update()

    def adicionar_novo_dado(e):
        
            hora = int(horarioCliente.value)
            dia = int(dataCliente.value)
            cliente = {"nome": f"{nomeCliente.value}", "dia": dia, "hora": hora}
            db.collection("users").document(f"{nomeCliente.value}").set(cliente)
            users_ref = db.collection("users")
            docs = users_ref.stream()

            for doc in docs:
                clientesAgendados.append(
                           [(doc.to_dict(),nomeCliente.value),
                            (doc.to_dict(),dataCliente.value),
                            (doc.to_dict(),horarioCliente.value)],
                            
                )
        
                print(f"{doc.id} => {doc.to_dict()}")
                print(clientesAgendados) 

            for informação in clientesAgendados:
                concatenar_dados = informação[1],informação[2]
                datasAgendadas.append(concatenar_dados) 


            hora = str(horarioCliente.value)
            dia = str(dataCliente.value)
            pagina.update()

    
        #atualizar a pagina

    def btn_click(e):  # função de verificação do botao "agendar"

        if not nomeCliente.value:
            nomeCliente.error_text = "Por favor, digite seu nome!"
        else:
            nome = nomeCliente.value

            doc_ref = db.collection("users").document(f"{nome}")

            doc = doc_ref.get()
            if doc.exists:

                text_resposta = Text(f"{nome} ja foi cadastrado!")
                pagina.clean()
                pagina.add(
                    Row([text_resposta], alignment=MainAxisAlignment.CENTER))
                pagina.add(
                    Row([botao_return], alignment=MainAxisAlignment.CENTER))
                pagina.update()   

            else:

                if not dataCliente.value:
                    dataCliente.error_text = "Por favor, escolha um dia!"
                else:
                    dataCliente.value = int(dataCliente.value)
                    if dataCliente.value <= 0 or dataCliente.value > 31 or dataCliente.value == 25:

                        text_resposta = Text(
                            f"Dia {dataCliente.value} não é uma data disponivel")
                        pagina.clean()
                        pagina.add(
                            Row([text_resposta], alignment=MainAxisAlignment.CENTER))
                        pagina.add(
                            Row([botao_return], alignment=MainAxisAlignment.CENTER))

                    elif dataCliente.value in domingos:
                        text_resposta = Text(
                            f"Não abrimos aos domingos!")
                        pagina.clean()
                        pagina.add(
                            Row([text_resposta], alignment=MainAxisAlignment.CENTER))
                        pagina.add(
                            Row([botao_return], alignment=MainAxisAlignment.CENTER))
                    else:

                        if not horarioCliente.value:
                            horarioCliente.error_text = "Por favor, digite um horario!"

                        else:
                            horarioCliente.value = int(horarioCliente.value)
                            if horarioCliente.value > 19 or horarioCliente.value < 9 or horarioCliente.value == 12:
                                text_resposta = Text(
                                    f"Esse horario não está disponivel")
                                pagina.clean()
                                pagina.add(
                                    Row([text_resposta], alignment=MainAxisAlignment.CENTER))
                                pagina.add(
                                    Row([botao_return], alignment=MainAxisAlignment.CENTER))

                            else:
                                adicionarDatas = dataCliente.value, horarioCliente.value
                                if adicionarDatas in datasAgendadas:
                                    text_resposta = Text(
                                        f"{horarioCliente.value}hrs está ocupado, escolha um horario vago!")
                                    pagina.clean()
                                    pagina.add(
                                        Row([text_resposta], alignment=MainAxisAlignment.CENTER))
                                    pagina.add(
                                        Row([botao_return], alignment=MainAxisAlignment.CENTER))

                                else:

                                    text_resposta = Text(
                                        f"Olá, {nomeCliente.value}. Você foi agendado para o dia {dataCliente.value} as {horarioCliente.value}:00 hrs!")
                                    pagina.clean()
                                    pagina.add(
                                        Row([text_resposta], alignment=MainAxisAlignment.CENTER))
                                    pagina.add(
                                        Row([botao_return], alignment=MainAxisAlignment.CENTER))

                                    adicionar_novo_dado(e)


                                
                                    

    # criar os itens que queremos na pagina
    nomeCliente = TextField(label="Seu Nome")
    dataCliente = TextField(label="Dia (Ex: 12)")
    horarioCliente = TextField(label="Horário (Ex: 13)")
    senhainput = TextField(label="Password", password=True)
    botao = ElevatedButton("Agendar", on_click=btn_click)
    botao_return = ElevatedButton("voltar", on_click=returnPage)
    #botao_entrar = ElevatedButton("entrar", on_click=entrar)
    #botao_cadastros = ElevatedButton("Sou o Barbeiro", on_click=cadastros)
    # adicionar os itens na pagina

    pagina.add(
        Row([Text("AGENDE SEU CORTE NO MÊS DE DEZEMBRO !")],
               alignment=MainAxisAlignment.CENTER),
        Row([nomeCliente], alignment=MainAxisAlignment.CENTER),
        Row([dataCliente], alignment=MainAxisAlignment.CENTER),
        Row([horarioCliente], alignment=MainAxisAlignment.CENTER),
        Row([botao], alignment=MainAxisAlignment.CENTER),
        #Row([botao_cadastros], alignment=MainAxisAlignment.CENTER),
    )
    pagina.update()



    
app(target=main,view=WEB_BROWSER)