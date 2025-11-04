import webview
from flask import Flask, request, render_template
import threading
import time
import copy

app = Flask(__name__)

class Matrizes:
    def __init__(self, colunas, linhas, lei=None):
        self.linhas = linhas
        self.colunas = colunas
        self.dados = [[0 for _ in range(colunas)]for _ in range(linhas)]
        if lei:
            for i in range(linhas):
                for j in range(colunas):
                    self.dados[i][j] = lei(i+1,j+1)
        self.steps = []
        self.time_taken = 0

    def __getitem__(self, i, j):
        return self.dados[i-1][j-1]
    
    def __setitem__(self, i, j, valor):
        self.dados[i-1][j-1] = valor

    def __str__(self):
        return '\n'.join([' '.join([str(elemento) for elemento in linha]) for linha in self.dados])
    
    def html_format(self):
        result = "&lt;div class='matrix'&gt;"
        for linha in self.dados:
            result += "&lt;div class='row'&gt;"
            for elem in linha:
                result += f"&lt;span class='element'&gt;{elem:.3f}&lt;/span&gt;"
            result += "&lt;/div&gt;"
        result += "&lt;/div&gt;"
        return result
    
    def add_step(self, description, matrix):
        self.steps.append((description, matrix.html_format()))

    def estimar_tempo_determinantes(self):
        """Estima o tempo necessário para calcular determinantes baseado em uma amostra"""
        import math
        import time
        
        # Cria uma matriz 3x3 para teste
        matriz_teste = Matrizes(3, 3)
        for i in range(3):
            for j in range(3):
                matriz_teste.dados[i][j] = 1
        
        # Mede o tempo para calcular o determinante 3x3
        inicio = time.time()
        matriz_teste.determinante()
        tempo_base = time.time() - inicio
        
        # Calcula fatorial do tamanho atual relativo ao teste
        fator_complexidade = math.factorial(self.linhas) / math.factorial(3)
        
        # Estima o tempo total
        tempo_estimado = tempo_base * fator_complexidade
        return tempo_estimado
    
    def determinante(self):
        if self.linhas != self.colunas:
            raise ValueError("Matriz não é quadrada")
        
        if self.linhas == 1:
            return self.dados[0][0]
        
        if self.linhas == 2:
            return self.dados[0][0] * self.dados[1][1] - self.dados[0][1] * self.dados[1][0]
        
        det = 0
        for j in range(self.colunas):
            cofator = self.dados[0][j]
            submatriz = Matrizes(self.colunas-1, self.linhas-1)
            for i in range(1, self.linhas):
                for k in range(self.colunas):
                    if k < j:
                        submatriz.dados[i-1][k] = self.dados[i][k]
                    elif k > j:
                        submatriz.dados[i-1][k-1] = self.dados[i][k]
            det += cofator * (-1)**(j) * submatriz.determinante()
        return det
        
    def estimar_tempo_escalonamento(self):
        """Estima o tempo necessário para escalonamento baseado em uma amostra"""
        import time
        
        # Cria uma matriz 3x3 para teste
        matriz_teste = Matrizes(3, 3)
        b_teste = [1, 1, 1]
        for i in range(3):
            for j in range(3):
                matriz_teste.dados[i][j] = 1
        
        # Mede o tempo para resolver o sistema 3x3
        inicio = time.time()
        matriz_teste.resolver_por_escalonamento(b_teste)
        tempo_base = time.time() - inicio
        
        # Calcula fator de complexidade O(n³) relativo ao teste
        fator_complexidade = (self.linhas ** 3) / (3 ** 3)
        
        # Estima o tempo total
        tempo_estimado = tempo_base * fator_complexidade
        return tempo_estimado

    def resolver_por_escalonamento(self, b):
        start_time = time.time()
        n = self.linhas
        matriz_aumentada = Matrizes(self.colunas + 1, self.linhas)
        
        # Criar matriz aumentada
        for i in range(self.linhas):
            for j in range(self.colunas):
                matriz_aumentada.dados[i][j] = self.dados[i][j]
            matriz_aumentada.dados[i][-1] = b[i]
        
        self.add_step("Matriz Aumentada Inicial", matriz_aumentada)
        
        # Escalonamento
        for i in range(n):
            # Encontrar pivô
            pivo = matriz_aumentada.dados[i][i]
            if abs(pivo) < 1e-10:
                for j in range(i + 1, n):
                    if abs(matriz_aumentada.dados[j][i]) > 1e-10:
                        matriz_aumentada.dados[i], matriz_aumentada.dados[j] = \
                            matriz_aumentada.dados[j], matriz_aumentada.dados[i]
                        self.add_step(f"Troca de linhas {i+1} ↔ {j+1}", matriz_aumentada)
                        break
                pivo = matriz_aumentada.dados[i][i]
                if abs(pivo) < 1e-10:
                    self.time_taken = time.time() - start_time
                    return "Sistema sem solução única"

            # Eliminar elementos abaixo do pivô
            for j in range(i + 1, n):
                fator = matriz_aumentada.dados[j][i] / pivo
                if abs(fator) > 1e-10:
                    for k in range(i, n + 1):
                        matriz_aumentada.dados[j][k] -= fator * matriz_aumentada.dados[i][k]
                    self.add_step(f"L{j+1} = L{j+1} - {fator:.3f}L{i+1}", matriz_aumentada)

        # Retrosubstituição
        x = [0] * n
        for i in range(n-1, -1, -1):
            soma = matriz_aumentada.dados[i][-1]
            for j in range(i+1, n):
                soma -= matriz_aumentada.dados[i][j] * x[j]
            x[i] = soma / matriz_aumentada.dados[i][i]
        
        self.time_taken = time.time() - start_time
        return x

    def resolver_por_determinantes(self, b):
        start_time = time.time()
        n = self.linhas
        det_principal = self.determinante()
        
        if abs(det_principal) < 1e-10:
            self.time_taken = time.time() - start_time
            return "Sistema sem solução única"
        
        x = []
        for i in range(n):
            matriz_temp = Matrizes(n, n)
            for j in range(n):
                for k in range(n):
                    if k == i:
                        matriz_temp.dados[j][k] = b[j]
                    else:
                        matriz_temp.dados[j][k] = self.dados[j][k]
            
            self.add_step(f"Matriz para x{i+1}", matriz_temp)
            det_i = matriz_temp.determinante()
            x.append(det_i / det_principal)
        
        self.time_taken = time.time() - start_time
        return x

def solve_with_timeout(metodo, *args, timeout=300):  # 5 minutos de timeout
    import signal

    def handler(signum, frame):
        raise TimeoutError("O cálculo excedeu o tempo limite")

    # Configurar o timeout
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(timeout)
    
    try:
        result = metodo(*args)
        signal.alarm(0)  # Desativa o alarme
        return result
    except TimeoutError as e:
        return str(e)
    finally:
        signal.alarm(0)  # Garante que o alarme está desativado

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        size = int(request.form.get('size', 2))
        matriz_a = Matrizes(size, size)
        b = []
        
        if request.form.get('estimar') == '1':
            # Apenas calcular estimativas
            tempo_est_escalonamento = matriz_a.estimar_tempo_escalonamento()
            tempo_est_determinantes = matriz_a.estimar_tempo_determinantes()
            return render_template('index.html',
                                size=size,
                                estimativa_escalonamento=tempo_est_escalonamento,
                                estimativa_determinantes=tempo_est_determinantes,
                                apenas_estimativa=True)
        
        # Preencher a matriz A e o vetor b
        try:
            for i in range(size):
                for j in range(size):
                    matriz_a.dados[i][j] = float(request.form.get(f'a{i}{j}', 0))
                b.append(float(request.form.get(f'b{i}', 0)))
        except ValueError:
            return render_template('index.html',
                                size=size,
                                error="Por favor, insira apenas números válidos")
        
        # Calcular estimativas
        tempo_est_escalonamento = matriz_a.estimar_tempo_escalonamento()
        tempo_est_determinantes = matriz_a.estimar_tempo_determinantes()
        
        # Resolver pelo método de escalonamento
        resultado_escalonamento = matriz_a.resolver_por_escalonamento(b)
        steps_escalonamento = matriz_a.steps
        tempo_escalonamento = matriz_a.time_taken
        
        matriz_a.steps = []  # Limpar steps para o próximo método
        if tempo_est_determinantes > 300:  # Se estimativa > 5 minutos
            resultado_determinantes = f"Tempo estimado muito alto: {tempo_est_determinantes:.1f} segundos"
            steps_determinantes = []
            tempo_determinantes = 0
        else:
            resultado_determinantes = matriz_a.resolver_por_determinantes(b)
            steps_determinantes = matriz_a.steps
            tempo_determinantes = matriz_a.time_taken
        
        return render_template('index.html',
                             size=size,
                             matriz_a=matriz_a.dados,
                             vetor_b=b,
                             resultado_escalonamento=resultado_escalonamento,
                             resultado_determinantes=resultado_determinantes,
                             steps_escalonamento=steps_escalonamento,
                             steps_determinantes=steps_determinantes,
                             tempo_escalonamento=tempo_escalonamento,
                             tempo_determinantes=tempo_determinantes)

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