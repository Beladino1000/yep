import tkinter as tk

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
    
def App():
    root = tk.Tk()
    root.title("Matriz")
    root.geometry("800x600")
    root.mainloop()

if __name__ == "__main__":
    App()
