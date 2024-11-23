import pandas as pd
import pickle
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
import uvicorn
from pydantic import BaseModel
import os

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

ID_USER = os.getenv("ID_USER", "Desconocida/o")

app = FastAPI()

class Answer(BaseModel):
    orderAmount : float
    orderState : str
    paymentMethodRegistrationFailure : str
    paymentMethodType : str
    paymentMethodProvider : str
    paymentMethodIssuer : str
    transactionAmount : int
    transactionFailed : bool
    emailDomain : str
    emailProvider : str
    customerIPAddressSimplified : str
    sameCity : str

@app.get("/")
async def root():
    return {"message": "Usuario/a" + ID_USER}


@app.post("/prediccion")
def predict_fraud_customer (answer:Answer):
    answer_dict = jsonable_encoder(answer)

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

    prediction = model.predict(single_instance_ohe)

    #Castear numpy.int64 a solo int
    type_of_fraud = int(prediction[0])

    type_of_fraud = "No" if type_of_fraud == 0 else "Sí" if type_of_fraud == 1 else "Warning"

    response = {"Tipo de fraude": type_of_fraud}

    return response

if __name__ == "__main__":
    uvicorn.run(app, host = "0.0.0.0", port = 7860)