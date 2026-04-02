from fastapi import FastAPI
import pandas as pd
from blockchain import Blockchain

app = FastAPI()
blockchain = Blockchain()

# Load CSV files
sales_df = pd.read_csv("sales_inventory.csv")
demand_df = pd.read_csv("demand_data.csv")


# -----------------------------
# Surplus Detection Logic
# -----------------------------
def detect_surplus():
    df = sales_df.copy()

    # Simple prediction logic
    df["predicted_remaining"] = df["inventory"] - (
        df["sales"] * df["expiry_days"]
    )

    df["surplus"] = df["predicted_remaining"] > 50

    surplus_items = df[df["surplus"] == True]

    return surplus_items[["item", "store", "predicted_remaining"]].to_dict(
        orient="records"
    )


# -----------------------------
# Demand Urgency Calculation
# -----------------------------
def calculate_urgency():
    df = demand_df.copy()

    df["urgency_score"] = (
        0.5 * df["poverty_rate"]
        + 0.3 * (df["ngo_requests"] / df["ngo_requests"].max())
        + 0.2 * df["weather_severity"]
    )

    df = df.sort_values(by="urgency_score", ascending=False)

    return df.head(3).to_dict(orient="records")


# -----------------------------
# API Endpoints
# -----------------------------

@app.get("/")
def home():
    return {"message": "FoodChain AI Backend Running"}


@app.get("/surplus")
def surplus():
    return detect_surplus()


@app.get("/urgency")
def urgency():
    return calculate_urgency()


@app.get("/redistribute")
def redistribute():
    surplus = detect_surplus()
    demand = calculate_urgency()

    if not surplus or not demand:
        return {"message": "No redistribution needed"}

    selected_surplus = surplus[0]
    selected_zone = demand[0]

    transaction = {
        "item": selected_surplus["item"],
        "from_store": selected_surplus["store"],
        "to_zone": selected_zone["area"],
        "quantity": int(selected_surplus["predicted_remaining"]),
    }

    block = blockchain.add_block(transaction)

    return {
        "redistribution": transaction,
        "block_hash": block.hash,
    }


@app.get("/blockchain")
def view_blockchain():
    return blockchain.get_chain()
