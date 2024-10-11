#   VINICIUS RODRIGUES DA COSTA
#   RAFAEL LUIZ CUYPERS

import tkinter as tk # biblioteca tkinter para interface grafica
import tkinter.font as tkFont # Biblioteca para alterar o tamanho da fonte
import random # biblioteca de randomização
import os  # biblioteca para chamada do sistema operacional
from salvamentoSys import salvamento  # importação do arquivo de salvamento

class Jogo(tk.Frame): # classe do jogo
    def __init__(self, master=None): # funçao mestre
        super().__init__(master)
        self.salvamento = salvamento(".pkl", "saved_data")  # Criando uma instância do salvamento
        self.carregar_palavras() # chama a funçao carregar palavras
        self.nova_palavra() # chama a funçao nova palavras
        self.pontos = 0 # variavel inicial pontos
        self.chances = 6 # variavel inicial chances

        if not os.path.exists(self.salvamento.save_folder): # procura o arquivo salvamento
            os.makedirs(self.salvamento.save_folder) # se nao existir cria um novo

        # barra de digitação
        self.entry_letra = tk.Entry(self.master, bg="white", font=("Arial", 12), bd=0)
        self.entry_letra.pack(pady=10, padx=20, ipadx=20, ipady=5)
        
        # botão ADIVINHAR
        self.button_adivinhar = tk.Button(self.master, text="Adivinhar", command=self.verificar_letra, bg="#4285f4", fg="white", font=("Arial", 12), bd=0, padx=20, pady=5)
        self.button_adivinhar.pack(pady=5)
        
        # botão SALVAR
        self.button_salvar = tk.Button(self.master, text="Salvar", command=self.salvar_jogo, bg="#4285f4", fg="white", font=("Arial", 12), bd=0, padx=20, pady=5)
        self.button_salvar.pack(pady=5)
        
        # botão CARREGAR
        self.button_carregar = tk.Button(self.master, text="Carregar", command=self.carregar_jogo, bg="#4285f4", fg="white", font=("Arial", 12), bd=0, padx=20, pady=5)
        self.button_carregar.pack(pady=5)
        
        # mostra o resultado
        self.label_resultado = tk.Label(self.master, text="", bg="#f1f1f1", font=("Arial", 12))
        self.label_resultado.pack()
        
        # mostra a pontuação
        self.pontuacao_label = tk.Label(self.master, text="Pontuação: 0", bg="#4285f4", fg="white", font=("Arial", 12),bd=0, padx=20, pady=5)
        self.pontuacao_label.pack()
        
        # mostra as chances
        self.chances_label = tk.Label(self.master, text="Chances: 6", bg="#4285f4", fg="white", font=("Arial", 12),bd=0, padx=20, pady=5)
        self.chances_label.pack(padx=10, pady=10)
        
        # mostra as categorias
        self.categoria_label = tk.Label(self.master, text="CATEGORIA: ", bg="#f1f1f1", font=("Arial", 12))
        self.categoria_label.pack(padx=10, pady=10)

    def carregar_palavras(self): # função carregar palavras
        self.palavras = {
            "animal": ["cachorro", "gato", "cavalo", "coelho"], # dicionário das palavras
            "frutas": ["maca", "uva", "banana", "morango"],
            "cores": ["azul", "amarelo", "vermelho", "rosa"],
            "objeto": ["tesoura", "frigideira", "bola", "mochila"]
        }

    def nova_palavra(self): # funçao nova palavra
        categoria = random.choice(list(self.palavras.keys()))
        self.palavra_atual = random.choice(self.palavras[categoria])
        self.letras_encontradas = set()

    def verificar_letra(self): # verificar letra
        letra = self.entry_letra.get().lower()

        if letra in self.palavra_atual: # verifica se a letra digitada esta na string
            self.letras_encontradas.add(letra)
            self.pontos += 1 # se sim + 1 ponto
            self.atualizar_resultado() # atualiza o resultado
        else:
            self.label_resultado.config(text=f"A letra '{letra}' não está na palavra.")
            self.chances -= 1 # se a letra não estiver -1 chance 

    def atualizar_resultado(self): # função atualizar resultado
        resultado = "" # espaço vazio começa
        for char in self.palavra_atual: # para cada letra na palavra
            if char in self.letras_encontradas: # se a letra esta na palavra adiciona o char no espaço resultado
                resultado += char + " "
            else:
                resultado += "_ " # se não mostra as letras faltantes 
        self.label_resultado.config(text=resultado) # atualiza o resultado na interface grafica
        self.pontuacao_label.config(text=f"Pontuação: {self.pontos}") # seta os pontos conforme o resultado
        self.chances_label.config(text=f"Chances: {self.chances}") # seta as chances na interface grafica
        self.categoria_label.config(text=f"CATEGORIA: {self.categoria_atual}") # seta a categoria

        if set(self.letras_encontradas) == set(self.palavra_atual): # verifica se todas as letras foram encontradas
            self.label_resultado.config(text="Parabéns! Você encontrou todas as letras.")
            self.nova_palavra()
            self.pontos = self.pontos
            self.chances = 6 # continua os pontos

    def salvar_jogo(self): # função de salvar o jogo
        data_to_save = (self.palavras, self.palavra_atual, list(self.letras_encontradas), self.pontos) #cria o nome do arquivo de salvamento
        self.salvamento.save_data(data_to_save, "game_data")
        print("Jogo salvo")


    def carregar_jogo(self):
        # carrega os dados do jogo
        saved_data = self.salvamento.load_game_data(["game_data"], (None,))
        if saved_data is not None:
            self.palavras, self.palavra_atual, letras_encontradas, self.pontos = saved_data

            # eonverte letras_encontradas de lista para conjunto
            self.letras_encontradas = set(letras_encontradas)

            # encontra a categoria da palavra atual
            for categoria, palavras_categoria in self.palavras.items():
                if self.palavra_atual in palavras_categoria:
                    self.categoria_atual = categoria
                    break

            # atualiza as informações na interface
            self.atualizar_resultado()
            self.categoria_label.config(text=f"CATEGORIA: {self.categoria_atual}")



class Janela(tk.Tk): # classe  da janela
    def __init__(self):
        super().__init__()
        self.title("Jogo da Forca")
        self.geometry("500x500")
        self.configure(bg="#f1f1f1")  # definindo a cor e o tamanho da janela

        # inicializa a janela
        self.game_frame = Jogo(self)
        self.game_frame.pack()

if __name__ == "__main__": # mantém a janela aberta
    app = Janela()
    app.mainloop()
