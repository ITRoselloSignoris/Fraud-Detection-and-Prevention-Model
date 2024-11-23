import requests

search_api_url = "http://127.0.0.1:7860/run/prediccion"

# CASO 1 -> Tipo de fraude: 0/False
data = {
    "data": [
        18.0,
        "pending",
        "True",
        "card",
        "JCB 16 digit",
        "Citizens First Banks",
        18,
        "False",
        "com",
        "yahoo",
        "only_letters",
        "yes"  
    ]
}

# CASO 2 -> Tipo de fraude: 1/True
data2 = {
    "data": [
        26.0,
        "fulfilled",
        "True",
        "bitcoin",
        "VISA 16 digit",
        "Solace Banks",
        26,
        "False",
        "com",
        "yahoo",
        "only_letters",
        "no" 
    ]
}

response1 = requests.post(search_api_url, json = data)
response1 = response1.json()
response1 = response1["data"][0]["label"]
print("Predicción: " + response1)

response2 = requests.post(search_api_url, json = data2)
response2 = response2.json()
response2 = response2["data"][0]["label"]
print("Predicción: " + response2)