"""
Cria imagem .gif com matriz de 50x50, 20 steps, 4 corações que diminuem

"""

# Importando as bibliotecas necessárias
import numpy as np
import matplotlib.pyplot as plt
import imageio
import os

# --- Classe principal do Jogo da Vida ---
class Game():
    def __init__(self, linhas, colunas) -> None:
        """
        Inicializa o tabuleiro do Jogo da Vida com um padrão de 4 corações.
        Args:
            linhas (int): Número de linhas do tabuleiro.
            colunas (int): Número de colunas do tabuleiro.
        """
        self.linhas = linhas
        self.colunas = colunas
        
        # 1. Começa com um grid totalmente vazio
        self.grid = np.zeros((linhas, colunas), dtype=int)

        # 2. Define o padrão do coração (o mesmo de antes)
        heart_pattern = np.array([
            [0, 1, 1, 0, 1, 1, 0],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [0, 1, 1, 1, 1, 1, 0],
            [0, 0, 1, 1, 1, 0, 0],
            [0, 0, 0, 1, 0, 0, 0]
        ], dtype=int)

        # Função auxiliar para colocar um padrão em uma posição
        def place_pattern(grid, pattern, center_row, center_col):
            pattern_height, pattern_width = pattern.shape
            start_row = center_row - pattern_height // 2
            start_col = center_col - pattern_width // 2
            
            # Garante que o padrão cabe no grid antes de colocar
            if start_row >= 0 and start_col >= 0 and \
               (start_row + pattern_height) <= grid.shape[0] and \
               (start_col + pattern_width) <= grid.shape[1]:
                grid[start_row : start_row + pattern_height, start_col : start_col + pattern_width] = pattern

        # 3. Define os centros dos 4 quadrantes para uma matriz 50x50
        quadrant_centers = [
            (12, 12), # Quadrante Superior Esquerdo
            (12, 37), # Quadrante Superior Direito
            (37, 12), # Quadrante Inferior Esquerdo
            (37, 37)  # Quadrante Inferior Direito
        ]

        # 4. Coloca um coração em cada centro
        for r, c in quadrant_centers:
            place_pattern(self.grid, heart_pattern, r, c)

    def update(self) -> None:
        """
        Aplica as regras do Jogo da Vida para avançar uma geração (step).
        (Esta função permanece a mesma)
        """
        new_grid = self.grid.copy()
        for i in range(self.linhas):
            for j in range(self.colunas):
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

                if self.grid[i, j] == 1 and (total_vizinhos < 2 or total_vizinhos > 3):
                    new_grid[i, j] = 0
                elif self.grid[i, j] == 0 and total_vizinhos == 3:
                    new_grid[i, j] = 1
        
        self.grid = new_grid

# --- Função para criar e salvar a animação ---
def criar_animacao(matriz_size, steps, output_filename):
    """
    Executa a simulação e gera um GIF animado.
    (Esta função permanece a mesma)
    """
    game = Game(matriz_size, matriz_size)
    frames = []

    print("Gerando frames para a animação...")
    for step_num in range(steps):
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.imshow(game.grid, cmap='binary')
        ax.set_title(f"Game of Life - Step: {step_num}", fontsize=16)
        ax.set_xticks([])
        ax.set_yticks([])

        fig.canvas.draw()

        width_float, height_float = fig.canvas.renderer.get_canvas_width_height()
        width = int(width_float)
        height = int(height_float)
        
        buffer = fig.canvas.tostring_argb()
        image_rgba = np.frombuffer(buffer, dtype='uint8').reshape(height, width, 4)
        frames.append(image_rgba[:, :, :3])

        plt.close(fig)
        game.update()
        print(f"  - Step {step_num + 1}/{steps} concluído.")

    print(f"\nSalvando animação em '{output_filename}'...")
    imageio.mimsave(output_filename, frames, fps=10)
    print("Animação salva com sucesso!")

# --- Execução Principal do Script ---
if __name__ == '__main__':
    # --- PARÂMETROS FIXOS DA SIMULAÇÃO ---
    matriz_size = 50
    total_steps = 20
    
    print(f"Iniciando simulação: Matriz de {matriz_size}x{matriz_size}, {total_steps} steps.")

    # --- Lógica para criar pasta e nome do arquivo (a mesma de antes) ---

    script_dir = os.path.dirname(__file__)
    project_root = os.path.dirname(script_dir)
    output_dir = os.path.join(project_root, 'figures', 'gif')
    os.makedirs(output_dir, exist_ok=True)

    # Cria o nome base do arquivo dinamicamente a partir do nome do script
    base_filename = os.path.splitext(os.path.basename(__file__))[0]

    version = 1
    while True:
        version_str = f"v{version:03d}"
        gif_filename = f"{base_filename}_{version_str}.gif"
        full_path = os.path.join(output_dir, gif_filename)
        if not os.path.exists(full_path):
            break
        version += 1
    
    # Chama a função principal com os valores fixos e o caminho versionado
    criar_animacao(matriz_size, total_steps, full_path)