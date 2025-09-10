# Importando as bibliotecas necessárias
import os
import time
import numpy as np
import matplotlib.pyplot as plt
import imageio
from math import floor
from random import random

# --- Classe principal do Jogo da Vida ---
class Game():
    def __init__(self, linhas, colunas, vivos_percent) -> None:
        """
        Inicializa o tabuleiro do Jogo da Vida.
        Args:
            linhas (int): Número de linhas do tabuleiro.
            colunas (int): Número de colunas do tabuleiro.
            vivos_percent (float): Percentual de células que devem começar vivas (0 a 100).
        """
        self.linhas = linhas
        self.colunas = colunas
        
        # Usando NumPy para criar o grid. É mais eficiente para operações com matrizes.
        # O grid terá valores 1 (vivo) e 0 (morto).
        self.grid = np.random.choice(
            [1, 0], 
            size=(linhas, colunas), 
            p=[vivos_percent / 100, 1 - (vivos_percent / 100)]
        )

    def update(self) -> None:
        """
        Aplica as regras do Jogo da Vida para avançar uma geração (step).
        """
        # Cria uma cópia do grid para calcular o próximo estado
        new_grid = self.grid.copy()

        for i in range(self.linhas):
            for j in range(self.colunas):
                # Contando os vizinhos vivos
                # O operador % (módulo) garante que o tabuleiro seja "infinito" (toroidal)
                # ou seja, a borda direita se conecta com a esquerda, e a superior com a inferior.
                total_vizinhos = int((
                    self.grid[(i-1) % self.linhas, (j-1) % self.colunas] +
                    self.grid[(i-1) % self.linhas, j % self.colunas] +
                    self.grid[(i-1) % self.linhas, (j+1) % self.colunas] +
                    self.grid[i % self.linhas, (j-1) % self.colunas] +
                    self.grid[i % self.linhas, (j+1) % self.colunas] +
                    self.grid[(i+1) % self.linhas, (j-1) % self.colunas] +
                    self.grid[(i+1) % self.linhas, j % self.colunas] +
                    self.grid[(i+1) % self.linhas, (j+1) % self.colunas]
                ))

                # Aplicando as regras de Conway
                # 1. Célula viva com menos de 2 vizinhos vivos morre (solidão).
                if self.grid[i, j] == 1 and (total_vizinhos < 2):
                    new_grid[i, j] = 0
                # 2. Célula viva com mais de 3 vizinhos vivos morre (superpopulação).
                elif self.grid[i, j] == 1 and (total_vizinhos > 3):
                    new_grid[i, j] = 0
                # 3. Célula morta com exatamente 3 vizinhos vivos se torna viva (reprodução).
                elif self.grid[i, j] == 0 and (total_vizinhos == 3):
                    new_grid[i, j] = 1
                # 4. Célula viva com 2 ou 3 vizinhos vivos sobrevive. (Não precisa de código, pois ela já é 1)
        
        # Atualiza o grid principal com o novo estado
        self.grid = new_grid

# --- Função para criar e salvar a animação (VERSÃO CORRIGIDA PARA MACOS) ---
def criar_animacao(matriz_size, alives_percent, steps, output_filename):
    """
    Executa a simulação e gera um GIF animado.
    Args:
        matriz_size (int): O tamanho da matriz quadrada.
        alives_percent (int): O percentual inicial de células vivas.
        steps (int): O número de gerações a serem simuladas.
        output_filename (str): O nome do arquivo .gif a ser salvo.
    """
    game = Game(matriz_size, matriz_size, alives_percent)
    frames = []

    print("Gerando frames para a animação...")
    for step_num in range(steps):
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.imshow(game.grid, cmap='binary') 
        ax.set_title(f"Game of Life - Step: {step_num}", fontsize=16)
        ax.set_xticks([])
        ax.set_yticks([])

        fig.canvas.draw()
        
        # Pega as dimensões FÍSICAS do renderer, após o desenho
        width_float, height_float = fig.canvas.renderer.get_canvas_width_height()
        width = int(width_float)
        height = int(height_float)
        
        buffer = fig.canvas.tostring_argb() # Pega o buffer de dados
        
        # Usa as dimensões físicas corretas (height, width) no reshape
        image_rgba = np.frombuffer(buffer, dtype='uint8').reshape(height, width, 4)
        
        frames.append(image_rgba[:, :, :3]) # Converte de RGBA para RGB
        # --- FIM DA CORREÇÃO ---
        
        plt.close(fig)
        game.update()
        print(f"  - Step {step_num + 1}/{steps} concluído.")

    print(f"\nSalvando animação em '{output_filename}'...")
    imageio.mimsave(output_filename, frames, fps=10)
    print("Animação salva com sucesso!")


# --- Execução Principal do Script ---
if __name__ == '__main__':
    # Coletando informações do usuário
    matriz_size = int(input('Qual será o tamanho da matriz quadrada? (sugestão: 50 a 200): '))
    alives = int(input('Qual o percentual de células vivas no início? (0 a 100): '))
    total_steps = int(input('Quantos steps (gerações) você quer simular no GIF? (sugestão: 100): '))
    
    # Nome do arquivo de saída
    gif_filename = "game_of_life.gif"

    # Chama a função principal que cria a animação
    criar_animacao(matriz_size, alives, total_steps, gif_filename)