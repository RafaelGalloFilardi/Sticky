import tkinter as tk
from tkinter import messagebox

# Dicionário da história
historia = {
    "inicio": {
        "texto": "Você acorda em uma floresta misteriosa. À sua frente há dois caminhos.",
        "opcoes": {
            "Seguir pela trilha da direita": "caverna",
            "Seguir pela trilha da esquerda": "aldeia"
        }
    },
    # ... outras cenas podem estar aqui
}

# Atualiza a interface com base em uma cena
def mostrar_cena(cena):
    if cena not in historia:
        messagebox.showerror("Erro", f"Cena '{cena}' não existe.")
        return

    texto_historia.set(historia[cena]["texto"])
    
    for widget in botoes_frame.winfo_children():
        widget.destroy()

    for opcao, proxima_cena in historia[cena]["opcoes"].items():
        btn = tk.Button(botoes_frame, text=opcao, width=40, command=lambda cena=proxima_cena: mostrar_cena(cena))
        btn.pack(pady=5)

# Função para adicionar uma nova cena
def adicionar_cena():
    id_cena = entrada_id.get().strip()
    texto_cena = entrada_texto.get("1.0", tk.END).strip()
    opcoes_brutas = entrada_opcoes.get("1.0", tk.END).strip()

    if not id_cena or not texto_cena:
        messagebox.showwarning("Aviso", "Preencha o ID e o texto da cena.")
        return

    opcoes = {}
    if opcoes_brutas:
        linhas = opcoes_brutas.splitlines()
        for linha in linhas:
            if '>' in linha:
                escolha, destino = linha.split('>', 1)
                opcoes[escolha.strip()] = destino.strip()

    historia[id_cena] = {
        "texto": texto_cena,
        "opcoes": opcoes
    }
    messagebox.showinfo("Sucesso", f"Cena '{id_cena}' adicionada com sucesso.")
    entrada_id.delete(0, tk.END)
    entrada_texto.delete("1.0", tk.END)
    entrada_opcoes.delete("1.0", tk.END)

# Função para remover uma cena
def remover_cena():
    id_remover = entrada_remover.get().strip()
    if id_remover in historia:
        del historia[id_remover]
        messagebox.showinfo("Removido", f"Cena '{id_remover}' foi removida.")
    else:
        messagebox.showwarning("Aviso", f"Cena '{id_remover}' não existe.")
    entrada_remover.delete(0, tk.END)

# GUI principal
janela = tk.Tk()
janela.title("Jogo de Escolhas - Editor")
janela.geometry("700x600")
janela.resizable(False, False)

texto_historia = tk.StringVar()
label_historia = tk.Label(janela, textvariable=texto_historia, wraplength=680, justify="left", font=("Arial", 12))
label_historia.pack(pady=10)

botoes_frame = tk.Frame(janela)
botoes_frame.pack()

mostrar_cena("inicio")

# ========== Seção para adicionar cenas ==========
frame_editor = tk.LabelFrame(janela, text="Adicionar Nova Cena", padx=10, pady=10)
frame_editor.pack(padx=10, pady=10, fill="both", expand=False)

tk.Label(frame_editor, text="ID da Cena:").grid(row=0, column=0, sticky="e")
entrada_id = tk.Entry(frame_editor, width=30)
entrada_id.grid(row=0, column=1)

tk.Label(frame_editor, text="Texto da Cena:").grid(row=1, column=0, sticky="ne")
entrada_texto = tk.Text(frame_editor, width=50, height=4)
entrada_texto.grid(row=1, column=1)

tk.Label(frame_editor, text="Opções (uma por linha, formato: Escolha > CenaID):").grid(row=2, column=0, sticky="ne")
entrada_opcoes = tk.Text(frame_editor, width=50, height=4)
entrada_opcoes.grid(row=2, column=1)

btn_adicionar = tk.Button(frame_editor, text="Adicionar Cena", command=adicionar_cena)
btn_adicionar.grid(row=3, column=1, pady=5, sticky="e")

# ========== Seção para remover cenas ==========
frame_remover = tk.LabelFrame(janela, text="Remover Cena", padx=10, pady=10)
frame_remover.pack(padx=10, pady=5, fill="both", expand=False)

tk.Label(frame_remover, text="ID da Cena a remover:").grid(row=0, column=0)
entrada_remover = tk.Entry(frame_remover, width=30)
entrada_remover.grid(row=0, column=1)

btn_remover = tk.Button(frame_remover, text="Remover Cena", command=remover_cena)
btn_remover.grid(row=0, column=2, padx=10)

janela.mainloop()
