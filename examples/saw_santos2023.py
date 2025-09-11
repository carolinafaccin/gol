import os
import time
from math import floor
from random import random

class Game():  
	def __init__(self, linhas, colunas, vivos) -> None:  
		self.linhas = linhas  
		self.colunas = colunas  
		self.celulas = [False if random() > (vivos/100) else True for _ in range(linhas * colunas)]

		for _ in range(linhas * colunas):
    			if random() > (vivos/100):  
      				celula = True  
    			else:  
      				celula = False

	def __repr__(self) -> str:  
		gridizinho = ''  
		for x in range(self.linhas):  
			for y in range(self.colunas):   
				gridizinho += '#' if self.celulas[x * self.colunas + y] else '.'  
				gridizinho +=' ' # isso é śo um espaço  
			gridizinho +='\n'  
		return gridizinho

	def update(self) -> list:  
		new_grid = [x for x in self.celulas]  
		for pos, val in enumerate(self.celulas):  
			alive_n = self.__alive_nbs(pos)  
			if val:  
				if alive_n < 2 or alive_n > 3:  
					new_grid[pos] = False  
			else:  
				if alive_n == 3:  
					new_grid[pos] = True  
			self.celulas = new_grid

	def __alive_nbs(self, pos):  
		par_ordenado = self.__into_to_coord(pos)  
		count = 0  
		vizinhos = []  
		for linha in range(par_ordenado[0]-1, par_ordenado[0]+2):  
			for coluna in range(par_ordenado[1]-1, par_ordenado[1]+2):  
				if linha < 0 or linha >= self.linhas or coluna >= self.colunas or coluna < 0:  
					continue  
				if (linha, coluna) == par_ordenado:  
					continue  
				vizinhos.append((linha, coluna))  
		r = []  
		for v in vizinhos:  
			r.append(v[0] *self.colunas +v[1])  
		for p in r:  
			if self.celulas[p]:  
				count += 1  
		return count

	def __into_to_coord(self, pos):  
		x = floor(pos/self.colunas)  
		y = pos % self.colunas  
		return x, y
	
if __name__ ==  '__main__':  
    matriz_size = int((input('Qual será o tamaho da Matriz? Se por número quebrado eu vou arrendodar. To logo avisando! Sugestão 0 - 100: ')))  
    alives = 0  
    while True:  
        alives = int((input('Quantos percentos de vivos você deseja? 0 - 100. Vai: ')))  
        if (alives > 100) or (alives < 0):  
            print("Precisa ser de ZERO a CEM. Para de bagunçar o jogo! Vai: ")  
        else:  
            break  
    grid = Game(matriz_size, matriz_size, alives)  
    while True:  
        print(grid)  
        grid.update()  
        time.sleep(0.5)  
        os.system('clear')