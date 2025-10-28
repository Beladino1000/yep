import webview
import os
from flask import Flask, request, 
class Matrizes:

    def __init__(self,colunas,linhas,lei=None):
        self.linhas=linhas
        self.colunas=colunas
        self.dados=[[0 for _ in range(colunas)]for _ in range(linhas)]
        if lei:
            for i in range(linhas):
                for j in range(colunas):
                    self.dados[i][j]=lei(i+1,j+1)

    def __getitem__(self,i,j):
        return self.dados[i-1][j-1]
    
    def __setitem__(self,i,j,valor):
        self.dados[i-1][j-1]=valor

    def __str__(self):
        return '\n'.join([' '.join([str(elemento) for elemento in linha]) for linha in self.dados])
    
class Api:
    def receber(self,texto):
        print(f'Recebi o texto: {texto}')
        resultado=texto.upper()
        return resultado
    
if __name__ == '__main__':
    api=Api()
    html_file = os.path.join(os.path.dirname(__file__), 'index.html')

    webview.create_window(
        'Calculadora de Matrizes',
        js_api=api,
        url=127.0.0.1,
        port=5000
        width=1080,
        height=720
    )

    webview.start()