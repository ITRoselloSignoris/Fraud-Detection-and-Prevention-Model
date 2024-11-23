import mlflow
import pandas as pd
import pickle
import os

#Load model, categories and bins
PARENT_FOLDER = os.path.dirname(__file__)
MODEL_PATH = os.path.join(PARENT_FOLDER, "../src/model/modelo_proyecto_final.pkl")
COLUMNS_PATH = os.path.join(PARENT_FOLDER, "../src/ohe_categories_without_fraudulent.pickle")
ORDER_BINS_PATH = os.path.join(PARENT_FOLDER, "../src/saved_bins/orderAmount_bins.pickle")
TRANSACTION_BINS_PATH = os.path.join(PARENT_FOLDER, "../src/saved_bins/transactionAmount_bins.pickle")

with open(MODEL_PATH, "rb") as handle:
    model = pickle.load(handle)

with open(ORDER_BINS_PATH, "rb") as handle:
    new_saved_bins_order = pickle.load(handle)

with open(TRANSACTION_BINS_PATH, "rb") as handle:
     new_saved_bins_transaction = pickle.load(handle)

with open(COLUMNS_PATH, "rb") as handle:
     ohe_tr = pickle.load(handle)

#Load model by Stage
model_name = "My_model"
stage = "Production"

loaded_model = mlflow.pyfunc.load_model(
    model_uri = f"models:/{model_name}/{stage}"
)

# Input data
data = {
    "orderAmount" : 18.0,
    "orderState" : "pending",
    "paymentMethodRegistrationFailure" : "True",
    "paymentMethodType" : "card",
    "paymentMethodProvider" : "JCB 16 digit",
    "paymentMethodIssuer" : "Citizens First Banks",
    "transactionAmount" : 18,
    "transactionFailed" : False,
    "emailDomain" : "com",
    "emailProvider" : "yahoo",
    "customerIPAddressSimplified" : "only_letters",
    "sameCity" : "yes"
}

data2 = {
    "orderAmount" : 26.0,
    "orderState" : "fulfilled",
    "paymentMethodRegistrationFailure" : "True",
    "paymentMethodType" : "bitcoin",
    "paymentMethodProvider" : "VISA 16 digit",
    "paymentMethodIssuer" : "Solace Banks",
    "transactionAmount" : 26,
    "transactionFailed" : False,
    "emailDomain" : "com",
    "emailProvider" : "yahoo",
    "customerIPAddressSimplified" : "only_letters",
    "sameCity" : "no"
}

#Prediction function
def predict_fraud_customer(data):
    answer_dict = data

    for key,value in answer_dict.items():
        answer_dict[key] = [value]

    #Crear dataframe
    single_instance = pd.DataFrame.from_dict(answer_dict)

    #Manejar puntos de corte/bins
    single_instance["orderAmount"] = single_instance["orderAmount"].astype(float)
    single_instance["orderAmount"] = pd.cut(single_instance["orderAmount"], bins = new_saved_bins_order, include_lowest = True)

    single_instance["transactionAmount"] = single_instance["transactionAmount"].astype(int)
    single_instance["transactionAmount"] = pd.cut(single_instance["transactionAmount"], bins = new_saved_bins_transaction, include_lowest = True)

    #One Hot Encoding
    single_instance_ohe = pd.get_dummies(single_instance).reindex(columns = ohe_tr).fillna(0)

    #Prediction
    prediction = loaded_model.predict(single_instance_ohe)

    #Castear numpy.int64 a solo int
    type_of_fraud = int(prediction[0])

    type_of_fraud = "No" if type_of_fraud == 0 else "Sí" if type_of_fraud == 1 else "Warning"

    response = {"Tipo de fraude": type_of_fraud}

    return response

print(predict_fraud_customer(data))
print(predict_fraud_customer(data2))