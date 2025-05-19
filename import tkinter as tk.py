import tkinter as tk

# Estrutura da história com escolhas
historia = {
    "inicio": {
        "texto": "Você acorda em uma floresta misteriosa. À sua frente há dois caminhos.",
        "opcoes": {
            "Seguir pela trilha da direita": "caverna",
            "Seguir pela trilha da esquerda": "aldeia"
        }
    },
    "caverna": {
        "texto": "Você encontra uma caverna escura. Há um barulho estranho lá dentro.",
        "opcoes": {
            "Entrar na caverna": "dragao",
            "Voltar e seguir o outro caminho": "aldeia"
        }
    },
    "aldeia": {
        "texto": "Você chega a uma pequena aldeia amigável. Os moradores parecem acolhedores.",
        "opcoes": {
            "Conversar com os aldeões": "sábio",
            "Ignorar e continuar andando": "floresta_profunda"
        }
    },
    "dragao": {
        "texto": "Um dragão aparece! Você tenta fugir, mas ele está bloqueando a saída.",
        "opcoes": {
            "Tentar conversar com o dragão": "amizade_dragao",
            "Atacar com uma espada encontrada no chão": "fim_ruim"
        }
    },
    "sábio": {
        "texto": "Um sábio lhe entrega um mapa mágico que leva até um tesouro escondido.",
        "opcoes": {
            "Seguir o mapa": "tesouro",
            "Agradecer e descansar na aldeia": "fim_paz"
        }
    },
    "floresta_profunda": {
        "texto": "Você se perde na floresta profunda. O clima esfria e escurece.",
        "opcoes": {
            "Gritar por ajuda": "sábio",
            "Continuar andando no escuro": "fim_ruim"
        }
    },
    "amizade_dragao": {
        "texto": "Surpreendentemente, o dragão é amigável e mostra uma saída secreta.",
        "opcoes": {
            "Seguir o dragão": "tesouro"
        }
    },
    "tesouro": {
        "texto": "Você encontra um antigo baú cheio de ouro e artefatos mágicos. Parabéns!",
        "opcoes": {}
    },
    "fim_paz": {
        "texto": "Você vive uma vida tranquila na aldeia, rodeado por novos amigos. Fim.",
        "opcoes": {}
    },
    "fim_ruim": {
        "texto": "Infelizmente, suas decisões levaram a um fim trágico. Mas toda história ensina algo. Fim.",
        "opcoes": {}
    }
}

# Função para atualizar a interface com base no estado da história
def mostrar_cena(cena):
    texto_historia.set(historia[cena]["texto"])
    
    for widget in botoes_frame.winfo_children():
        widget.destroy()
    
    for opcao, proxima_cena in historia[cena]["opcoes"].items():
        btn = tk.Button(botoes_frame, text=opcao, width=40, command=lambda cena=proxima_cena: mostrar_cena(cena))
        btn.pack(pady=5)

# Interface gráfica com tkinter
janela = tk.Tk()
janela.title("A Jornada do Herói")
janela.geometry("600x400")
janela.resizable(False, False)

texto_historia = tk.StringVar()
label_historia = tk.Label(janela, textvariable=texto_historia, wraplength=580, justify="left", font=("Arial", 12))
label_historia.pack(pady=20)

botoes_frame = tk.Frame(janela)
botoes_frame.pack()

# Começa a história
mostrar_cena("inicio")

janela.mainloop()
