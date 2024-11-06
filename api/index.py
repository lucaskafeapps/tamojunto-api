from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def gerar_token():
    url_token = "https://api.datacast3.com/api/Token/GerarToken"
    headers_token = {
        "Content-Type": "application/json"
    }
    data_token = {
        "chave": "VGVzdGVTb011bHRhczpoUUNmUmp2Tw=="
    }

    response = requests.post(url_token, headers=headers_token, json=data_token)
    if response.status_code == 200:
        response_data = response.json()
        if response_data.get("status") == "ok":
            return response_data.get("token")
        else:
            print("Erro ao gerar o token:", response_data.get("message"))
            return None
    else:
        print("Erro na requisição para gerar o token:", response.status_code)
        return None

def consultar_placa(placa):
    token = gerar_token()
    if token is None:
        return {"error": "Token não gerado"}

    url_placa = f"https://api.datacast3.com/api/v1.0/CodificacaoFipe/placa/{placa}"
    headers_placa = {
        "Authorization": f"Bearer {token}",
        "infocar-id-Key": "225"
    }

    response = requests.get(url_placa, headers=headers_placa)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Erro na requisição para consultar a placa", "status_code": response.status_code}

@app.route('/consulta_placa', methods=['GET'])
def consulta_placa():
    placa = request.args.get('placa')
    if not placa:
        return jsonify({"error": "Parâmetro 'placa' é obrigatório"}), 400

    resultado = consultar_placa(placa)
    return jsonify(resultado)

# Para que o Vercel entenda o app Flask
app = app