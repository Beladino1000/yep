import webview
import os
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

if __name__ == '__main__':

    html_file = os.path.join(os.path.dirname(__file__), 'index.html')

    webview.create_window(
        'Calculadora de Matrizes',
        js_api=Matrizes,
        url=html_file,
        width=800,
        height=600
    )

    webview.start()