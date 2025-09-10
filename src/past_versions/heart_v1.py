# Importando as bibliotecas necessárias
import numpy as np
import matplotlib.pyplot as plt
import imageio
import os # <-- Adicionamos o módulo 'os'

# --- Classe principal do Jogo da Vida ---
class Game():
    def __init__(self, linhas, colunas) -> None:
        """
        Inicializa o tabuleiro do Jogo da Vida com um padrão de coração no centro.
        Args:
            linhas (int): Número de linhas do tabuleiro.
            colunas (int): Número de colunas do tabuleiro.
        """
        self.linhas = linhas
        self.colunas = colunas
        
        # 1. Começa com um grid totalmente vazio (todas as células mortas)
        self.grid = np.zeros((linhas, colunas), dtype=int)

        # 2. Define o padrão do coração como uma matriz de 1s e 0s
        heart_pattern = np.array([
            [0, 1, 1, 0, 1, 1, 0],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [0, 1, 1, 1, 1, 1, 0],
            [0, 0, 1, 1, 1, 0, 0],
            [0, 0, 0, 1, 0, 0, 0]
        ], dtype=int)

        # 3. Calcula a posição para centralizar o coração
        pattern_height, pattern_width = heart_pattern.shape
        start_row = (linhas - pattern_height) // 2
        start_col = (colunas - pattern_width) // 2

        # Garante que o padrão cabe no grid
        if linhas > pattern_height and colunas > pattern_width:
            # 4. "Cola" o padrão do coração no grid principal usando slicing do NumPy
            self.grid[start_row : start_row + pattern_height, start_col : start_col + pattern_width] = heart_pattern

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
    # Coletando informações do usuário
    matriz_size = int(input('Qual será o tamanho da matriz quadrada? (sugestão: 80 ou mais): '))
    total_steps = int(input('Quantos steps (gerações) você quer simular no GIF? (sugestão: 100): '))
    
    # --- LÓGICA NOVA PARA CRIAR PASTA E NOME DO ARQUIVO ---

    # A. Define o diretório de saída
    # Pega o diretório do script atual (.../gol/src)
    script_dir = os.path.dirname(__file__)
    # Sobe um nível para o diretório raiz do projeto (.../gol)
    project_root = os.path.dirname(script_dir)
    # Cria o caminho para a pasta de saída
    output_dir = os.path.join(project_root, 'figures', 'gif')

    # Cria o diretório se ele não existir
    os.makedirs(output_dir, exist_ok=True)

    # B. Cria o nome base do arquivo a partir do nome do script
    # Ex: 'gol_heart_gif.py' -> 'gol_heart_gif'
    base_filename = os.path.splitext(os.path.basename(__file__))[0]

    # C. Encontra a próxima versão disponível
    version = 1
    while True:
        # Formata o número da versão com 3 dígitos (ex: 1 -> '001')
        version_str = f"v{version:03d}"
        # Monta o nome do arquivo com a versão
        gif_filename = f"{base_filename}_{version_str}.gif"
        # Monta o caminho completo do arquivo
        full_path = os.path.join(output_dir, gif_filename)

        # Verifica se um arquivo com esse nome já existe
        if not os.path.exists(full_path):
            break # Se não existe, encontramos o nome certo e saímos do loop
        version += 1 # Se existe, tenta a próxima versão
    
    # Chama a função principal com o caminho completo e versionado
    criar_animacao(matriz_size, total_steps, full_path)