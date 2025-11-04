import webview
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    """Serve a página principal."""
    return render_template('index.html')

def main():
    window = webview.create_window(
        'Meu App Híbrido Flask',
        app
        )
    
    webview.start()

if __name__ == '__main__':
    main()