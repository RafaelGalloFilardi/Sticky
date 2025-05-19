import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import os

# Estrutura da história com suporte a imagem
historia = {
    "inicio": {
        "texto": "Você acorda em uma floresta misteriosa.",
        "opcoes": {
            "Seguir pela trilha da direita": "caverna",
            "Seguir pela trilha da esquerda": "aldeia"
        },
        "imagem": None  # Caminho da imagem ou None
    }
}

# Armazenamento da imagem atual para evitar descarte do objeto
imagem_atual = None

def mostrar_cena(cena):
    global imagem_atual

    if cena not in historia:
        messagebox.showerror("Erro", f"Cena '{cena}' não existe.")
        return

    dados = historia[cena]
    texto_historia.set(dados["texto"])

    # Limpa botões anteriores
    for widget in botoes_frame.winfo_children():
        widget.destroy()

    for opcao, proxima_cena in dados["opcoes"].items():
        btn = tk.Button(botoes_frame, text=opcao, width=40, command=lambda cena=proxima_cena: mostrar_cena(cena))
        btn.pack(pady=5)

    # Atualiza a imagem de fundo se houver
    if dados.get("imagem"):
        try:
            imagem = Image.open(dados["imagem"])
            imagem = imagem.resize((700, 200), Image.ANTIALIAS)
            imagem_atual = ImageTk.PhotoImage(imagem)
            fundo_label.config(image=imagem_atual)
        except Exception as e:
            fundo_label.config(image="")
            imagem_atual = None
            print("Erro ao carregar imagem:", e)
    else:
        fundo_label.config(image="")
        imagem_atual = None

def adicionar_cena():
    id_cena = entrada_id.get().strip()
    texto_cena = entrada_texto.get("1.0", tk.END).strip()
    opcoes_brutas = entrada_opcoes.get("1.0", tk.END).strip()
    caminho_imagem = entrada_imagem.get().strip()

    if not id_cena or not texto_cena:
        messagebox.showwarning("Aviso", "ID e Texto são obrigatórios.")
        return

    opcoes = {}
    if opcoes_brutas:
        for linha in opcoes_brutas.splitlines():
            if '>' in linha:
                escolha, destino = linha.split('>', 1)
                opcoes[escolha.strip()] = destino.strip()

    historia[id_cena] = {
        "texto": texto_cena,
        "opcoes": opcoes,
        "imagem": caminho_imagem if caminho_imagem else None
    }

    messagebox.showinfo("Cena adicionada", f"Cena '{id_cena}' criada com sucesso!")
    entrada_id.delete(0, tk.END)
    entrada_texto.delete("1.0", tk.END)
    entrada_opcoes.delete("1.0", tk.END)
    entrada_imagem.delete(0, tk.END)

def remover_cena():
    id_remover = entrada_remover.get().strip()
    if id_remover in historia:
        del historia[id_remover]
        messagebox.showinfo("Removida", f"Cena '{id_remover}' foi removida.")
    else:
        messagebox.showwarning("Aviso", f"Cena '{id_remover}' não existe.")
    entrada_remover.delete(0, tk.END)

def escolher_imagem():
    caminho = filedialog.askopenfilename(filetypes=[("Imagens", "*.png;*.jpg;*.jpeg;*.gif")])
    if caminho:
        entrada_imagem.delete(0, tk.END)
        entrada_imagem.insert(0, caminho)

# ========== GUI ==========
janela = tk.Tk()
janela.title("Jogo Interativo com Plano de Fundo")
janela.geometry("720x700")
janela.resizable(False, False)

# Imagem de fundo
fundo_label = tk.Label(janela)
fundo_label.pack()

# Texto da cena
texto_historia = tk.StringVar()
label_historia = tk.Label(janela, textvariable=texto_historia, wraplength=680, justify="left", font=("Arial", 12))
label_historia.pack(pady=10)

# Botões da cena
botoes_frame = tk.Frame(janela)
botoes_frame.pack()

mostrar_cena("inicio")

# Adicionar Cena
frame_editor = tk.LabelFrame(janela, text="Adicionar Nova Cena", padx=10, pady=10)
frame_editor.pack(padx=10, pady=10, fill="both")

tk.Label(frame_editor, text="ID da Cena:").grid(row=0, column=0, sticky="e")
entrada_id = tk.Entry(frame_editor, width=30)
entrada_id.grid(row=0, column=1)

tk.Label(frame_editor, text="Texto da Cena:").grid(row=1, column=0, sticky="ne")
entrada_texto = tk.Text(frame_editor, width=50, height=4)
entrada_texto.grid(row=1, column=1)

tk.Label(frame_editor, text="Opções (Escolha > CenaID):").grid(row=2, column=0, sticky="ne")
entrada_opcoes = tk.Text(frame_editor, width=50, height=4)
entrada_opcoes.grid(row=2, column=1)

tk.Label(frame_editor, text="Imagem (caminho opcional):").grid(row=3, column=0, sticky="e")
entrada_imagem = tk.Entry(frame_editor, width=40)
entrada_imagem.grid(row=3, column=1, sticky="w")
btn_buscar_img = tk.Button(frame_editor, text="Procurar", command=escolher_imagem)
btn_buscar_img.grid(row=3, column=2)

btn_adicionar = tk.Button(frame_editor, text="Adicionar Cena", command=adicionar_cena)
btn_adicionar.grid(row=4, column=1, pady=5, sticky="e")

# Remover Cena
frame_remover = tk.LabelFrame(janela, text="Remover Cena", padx=10, pady=10)
frame_remover.pack(padx=10, pady=5, fill="both")

tk.Label(frame_remover, text="ID da Cena a remover:").grid(row=0, column=0)
entrada_remover = tk.Entry(frame_remover, width=30)
entrada_remover.grid(row=0, column=1)

btn_remover = tk.Button(frame_remover, text="Remover Cena", command=remover_cena)
btn_remover.grid(row=0, column=2, padx=10)

janela.mainloop()

import openai
import requests

openai.api_key = "SUA_CHAVE_DE_API_AQUI"  # Substitua pela sua chave

def gerar_imagem_ia(descricao, nome_arquivo):
    try:
        print("Gerando imagem com IA...")
        resposta = openai.Image.create(
            prompt=descricao,
            n=1,
            size="512x512"
        )
        url_imagem = resposta['data'][0]['url']
        
        # Baixa a imagem e salva localmente
        img_data = requests.get(url_imagem).content
        with open(nome_arquivo, 'wb') as handler:
            handler.write(img_data)
        
        print("Imagem gerada com sucesso:", nome_arquivo)
        return nome_arquivo
    except Exception as e:
        print("Erro ao gerar imagem:", e)
        return None
