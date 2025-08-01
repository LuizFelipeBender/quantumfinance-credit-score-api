
import os
import pandas as pd
import joblib
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import mlflow
import mlflow.sklearn

# Caminho dos dados
DATA_PATH = "dataset/raw/train.csv"
MODEL_DIR = "models"

def preprocess_data(df):
    # Colunas que usaremos no modelo
    features = [
        "Annual_Income", "Monthly_Inhand_Salary", "Num_Bank_Accounts",
        "Num_Credit_Card", "Interest_Rate", "Num_of_Loan", "Delay_from_due_date",
        "Num_of_Delayed_Payment", "Changed_Credit_Limit", "Num_Credit_Inquiries",
        "Credit_Utilization_Ratio", "Outstanding_Debt", "Monthly_Balance", "Age"
    ]

    # Remover outliers e valores inválidos
    df = df.copy()
    df = df[df["Age"] > 0]
    df = df[df["Monthly_Inhand_Salary"].notnull()]
    df = df[df["Credit_Score"].isin(["Poor", "Standard", "Good"])]

    df = df[features + ["Credit_Score"]].dropna()

    # Separar X e y
    X = df[features]
    y_raw = df["Credit_Score"]

    # Codificar o target
    le = LabelEncoder()
    y = le.fit_transform(y_raw)

    return X, y, le

def train():
    print("🚀 Iniciando treinamento...")

    # Ler dados
    df = pd.read_csv(DATA_PATH)
    X, y, label_encoder = preprocess_data(df)

    # Divisão treino/teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Modelo
    clf = RandomForestClassifier(random_state=42)
    clf.fit(X_train, y_train)
    accuracy = clf.score(X_test, y_test)
    print(f"✅ Acurácia: {accuracy:.4f}")

    # Criar pasta de modelos
    os.makedirs(MODEL_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Salvar modelo
    model_path = f"{MODEL_DIR}/model_{timestamp}.pkl"
    joblib.dump(clf, model_path)
    joblib.dump(clf, f"{MODEL_DIR}/model_latest.pkl")
    joblib.dump(label_encoder, f"{MODEL_DIR}/label_encoder.pkl")
    print(f"💾 Modelo salvo em {model_path}")

    # MLflow
    mlflow.set_tracking_uri("http://localhost:5000")
    with mlflow.start_run():
        mlflow.log_param("model", "RandomForestClassifier")
        mlflow.log_metric("accuracy", accuracy)
        mlflow.sklearn.log_model(clf, "model")
        print("📊 Modelo registrado no MLflow.")

if __name__ == "__main__":
    train()
