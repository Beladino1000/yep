import tkinter as tk
from tkinter import HtmlFrame
import os

class Matrizes:
    def __init__(self,colunas,linhas,lei=None):
        self.linhas=linhas
        self.colunas=colunas
        self.dados=[[0 for _ in range(colunas)]for _ in range(linhas)]
    def __getitem__(self,i,j):
        return self.dados[i-1][j-1]
    def __setitem__(self,i,j,valor):
        self.dados[i-1][j-1]=valor
    def __str__(self):
        return '\n'.join([' '.join([str(elemento) for elemento in linha]) for linha in self.dados])
    
root = tk.Tk()
root.title("Carregando HTML/CSS Local")
root.geometry("800x600")

browser_frame = HtmlFrame(root, messages_enabled=False) 
browser_frame.pack(fill="both", expand=True)

html_file_path = os.path.abspath('index.html')
browser_frame.load_file(f'file://{html_file_path}')

root.mainloop()