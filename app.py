from flask import Flask, request, jsonify
import requests
import sqlite3

from sekret.key import DATABASE, API_TOKEN_SANDBOX

app = Flask(__name__)

def get_available_services():
    """
    Получение списка доступных сервисов через API imeicheck.net.
    Возвращает словарь, список доступных сервисов или пустой словарь при ошибке.
    """
    url = "https://api.imeicheck.net/v1/services"
    headers = {"Authorization": f"Bearer {API_TOKEN_SANDBOX}"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Ошибка получения сервисов: {e}")
        return {}



def check_imei(imei, service_id):
    """
    Проверка IMEI через API imeicheck.net.
    Args:
        imei (str): IMEI номер для проверки.
        service_id (int): ID сервиса для проверки.

    Returns:
        dict: Ответ от API с информацией об устройстве.
    """
    url = "https://api.imeicheck.net/v1/checks"
    payload = {
        "deviceId": imei,
        "serviceId": service_id
    }
    headers = {"Authorization": f"Bearer {API_TOKEN_SANDBOX}"}

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Ошибка проверки IMEI: {e}")
        return {"error": "Ошибка проверки IMEI"}



def is_authorized(token):
    """
    Проверка токена авторизации.
    Args:
        token (str): Токен авторизации.
    Returns:
        bool: True, если токен авторизован, иначе False.
    """
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tokens WHERE token=?", (token,))
        result = cursor.fetchone()
        conn.close()
        if result is None:
            print(f"Unauthorized token: {token}")
            return False
        print(f"Authorized token: {token}")
        return True
    except sqlite3.Error as e:
        print(f"Ошибка работы с базой данных: {e}")
        return False



@app.route('/api/check-imei', methods=['POST'])
def api_check_imei():
    """
    Эндпоинт для проверки IMEI через API.
    Получает IMEI и токен авторизации от клиента, проверяет токен,
    выбирает подходящий сервис и выполняет запрос проверки IMEI.
    Returns:
        Response: JSON с результатами проверки IMEI или ошибкой.
    """
    data = request.json
    imei = data.get("imei")
    token = data.get("token")

    # Проверка наличия обязательных параметров
    if not imei or not token:
        return jsonify({"error": "Missing imei or token"}), 400

    # Проверка токена авторизации
    if not is_authorized(token):
        return jsonify({"error": "Unauthorized"}), 403

    # Получение списка доступных сервисов
    services = get_available_services()
    if not services:
        return jsonify({"error": "Unable to retrieve services"}), 500

    # Поиск подходящего mock-сервиса
    service_id = None
    for service in services:
        if "Mock" in service["title"]:  # Проверяем, что это тестовый сервис
            service_id = service["id"]
            break

    if not service_id:
        return jsonify({"error": "No suitable service found"}), 400

    # Проверка IMEI через выбранный сервис
    imei_data = check_imei(imei, service_id)
    return jsonify(imei_data)


if __name__ == "__main__":
    app.run(debug=True)