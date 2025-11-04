import webview
from flask import Flask, request, render_template
import threading

app = Flask(__name__)

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

@app.route('/')
def index():
    ordem=2
    matriz=Matrizes(ordem,ordem,0)
    print(matriz)
    return render_template('index.html',matriz=matriz)

def start_flask():
    app.run(host='127.0.0.1', port=5000)

if __name__ == '__main__':
    
    t = threading.Thread(target=start_flask)
    t.daemon = True
    t.start()

    window=webview.create_window(
        'Calculadora de Matrizes',
        'http://127.0.0.1:5000/',
        width=1080,
        height=720,
        resizable=True
        )

    webview.start()