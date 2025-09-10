# Importando as bibliotecas necessárias
import os
import numpy as np
import matplotlib.pyplot as plt
import imageio

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
        
        self.grid = np.random.choice(
            [1, 0], 
            size=(linhas, colunas), 
            p=[vivos_percent / 100, 1 - (vivos_percent / 100)]
        )

    def update(self) -> None:
        """
        Aplica as regras do Jogo da Vida para avançar uma geração (step).
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
def criar_animacao(matriz_size, alives_percent, steps, output_path):
    """
    Executa a simulação e gera um GIF animado.
    Args:
        matriz_size (int): O tamanho da matriz quadrada.
        alives_percent (int): O percentual inicial de células vivas.
        steps (int): O número de gerações a serem simuladas.
        output_path (str): O caminho COMPLETO onde o arquivo .gif será salvo.
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
        
        width_float, height_float = fig.canvas.renderer.get_canvas_width_height()
        width = int(width_float)
        height = int(height_float)
        
        buffer = fig.canvas.tostring_argb()
        image_rgba = np.frombuffer(buffer, dtype='uint8').reshape(height, width, 4)
        
        frames.append(image_rgba[:, :, :3])
        
        plt.close(fig)
        game.update()
        print(f"  - Step {step_num + 1}/{steps} concluído.")

    # Mensagem de salvamento atualizada para mostrar o caminho completo
    print(f"\nSalvando animação em '{output_path}'...")
    imageio.mimsave(output_path, frames, fps=10)
    print("Animação salva com sucesso!")


# --- Execução Principal do Script ---
if __name__ == '__main__':
    # --- NOVA LÓGICA PARA ORGANIZAÇÃO DE ARQUIVOS ---

    # 1. Define o diretório de saída
    # '..' significa 'subir um nível'. Como o script está em 'src',
    # subimos para 'gol' e então entramos em 'figures/gif'.
    output_dir = os.path.join('..', 'figures', 'gif')

    # 2. Cria o diretório se ele não existir
    # exist_ok=True evita um erro caso a pasta já exista
    os.makedirs(output_dir, exist_ok=True)

    # 3. Define o nome base do arquivo a partir do nome do script
    # __file__ é o nome do script atual (ex: 'gol_gif.py')
    base_name = os.path.splitext(os.path.basename(__file__))[0]

    # 4. Encontra o próximo número de versão disponível
    version = 1
    while True:
        # Formata o número da versão com 3 dígitos (ex: 1 -> '001')
        version_str = f"v{version:03d}"
        gif_filename = f"{base_name}_{version_str}.gif"
        
        # Constrói o caminho completo do arquivo
        full_path = os.path.join(output_dir, gif_filename)
        
        # Verifica se um arquivo com este nome já existe
        if not os.path.exists(full_path):
            break # Se não existe, encontramos nosso nome e saímos do loop
        
        version += 1 # Se existe, tenta o próximo número

    # --- FIM DA NOVA LÓGICA ---

    # Coletando informações do usuário
    matriz_size = int(input('Qual será o tamanho da matriz quadrada? (sugestão: 50 a 200): '))
    alives = int(input('Qual o percentual de células vivas no início? (0 a 100): '))
    total_steps = int(input('Quantos steps (gerações) você quer simular no GIF? (sugestão: 100): '))
    
    # Chama a função principal com o caminho completo e versionado
    criar_animacao(matriz_size, alives, total_steps, full_path)