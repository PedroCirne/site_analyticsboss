import os
from flask import Flask, request, send_file
from PIL import Image
import tempfile

app = Flask(_name_)
UPLOAD_FOLDER = 'uploads'

# Cria a pasta de upload se não existir
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def compress_image(input_path, target_size_kb):
    target_size_bytes = target_size_kb * 1024  # Converte KB para bytes
    
    with Image.open(input_path) as img:
        quality = 95
        while True:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
                temp_filename = temp_file.name
                img.save(temp_filename, 'JPEG', quality=quality)
                size = os.path.getsize(temp_filename)
                
                if size <= target_size_bytes or quality <= 5:
                    break
                
                quality -= 5
    return temp_filename

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "Nenhum arquivo selecionado"
        file = request.files['file']
        if file.filename == '':
            return "Nenhum arquivo selecionado"
        if file:
            try:
                target_size_kb = int(request.form['size_kb'])
                input_path = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(input_path)
                compressed_path = compress_image(input_path, target_size_kb)
                return send_file(compressed_path, as_attachment=True, download_name=f"{os.path.splitext(file.filename)[0]}_compressed_byordep.jpg")
            except Exception as e:
                error_message = str(e)
                return f'''
                <script>
                    alert("Erro: {error_message}");
                    window.history.back();
                </script>
                '''
    return '''
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Compactador de Imagens</title>
        <style>
            body {
                background-color: #90A262;
                color: #D9CD57;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 100vh;
                font-family: Arial, sans-serif;
                margin: 0;
                text-align: center;
            }
            header {
                width: 100%;
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 10px 20px;
                box-sizing: border-box;
                position: absolute;
                top: 0;
                background-color: #90A262;
            }
            h1 {
                font-weight: bold;
                color: #2B2D2A;
            }
            form {
                background-color: #2B2D2A;
                padding: 20px;
                border-radius: 10px;
                margin-top: 60px;
            }
            input[type="file"], input[type="text"], input[type="submit"] {
                display: block;
                margin: 10px auto;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            input[type="submit"] {
                background-color: #D9CD57;
                color: #2B2D2A;
                cursor: pointer;
            }
            input[type="submit"]:hover {
                background-color: #B8A644;
            }
            .designer {
                color: #D9CD57;
            }
        </style>
        <script>
            function showMessage(message) {
                alert(message);
            }
        </script>
    </head>
    <body>
        <header>
            <div></div> <!-- Placeholder para manter o espaço -->
            <div class="designer">Designed by ordep</div>
        </header>
        <div>
            <h1>Compactador de Imagens</h1>
            <form method="post" enctype="multipart/form-data" onsubmit="showMessage('Imagem compactada com sucesso!')">
                <label for="file">Escolha uma imagem:</label>
                <input type="file" name="file" required>
                <label for="size_kb">Tamanho desejado (KB):</label>
                <input type="text" name="size_kb" required>
                <input type="submit" value="Compactar">
            </form>
        </div>
    </body>
    </html>
    '''

if _name_ == '_main_':
    app.run(debug=True)

#TESTE