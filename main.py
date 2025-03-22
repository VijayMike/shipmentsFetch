from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import sqlite3

app = FastAPI(title="Shipping API")

class ShippingRequest(BaseModel):
    product_name: str
    quantity: int
    destination: str
    customer_name: str
    priority: Optional[str] = "normal"  

def init_db():
    conn = sqlite3.connect('shipments.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS shipments
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT,
                quantity INTEGER,
                destination TEXT,
                customer_name TEXT,
                priority TEXT,
                status TEXT,
                created_at TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.get("/")
def read_root():
    return {"message": "Welcome to Shipping API"}

@app.post("/shipments/")
async def create_shipment(shipment: ShippingRequest):
    conn = sqlite3.connect('shipments.db')
    c = conn.cursor()
    
    shipment_dict = shipment.dict()
    shipment_dict["status"] = "pending"
    shipment_dict["created_at"] = datetime.now().isoformat()
    
    c.execute('''INSERT INTO shipments (product_name, quantity, destination, 
                customer_name, priority, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (shipment_dict["product_name"],
            shipment_dict["quantity"],
            shipment_dict["destination"],
            shipment_dict["customer_name"],
            shipment_dict["priority"],
            shipment_dict["status"],
            shipment_dict["created_at"]))
    
    shipment_id = c.lastrowid
    conn.commit()
    conn.close()
    
    shipment_dict["id"] = shipment_id
    return {
        "message": "Shipment created successfully",
        "shipment": shipment_dict
    }

@app.get("/shipments/")
async def get_shipments():
    conn = sqlite3.connect('shipments.db')
    c = conn.cursor()
    c.execute("SELECT * FROM shipments")
    columns = [description[0] for description in c.description]
    shipments = [dict(zip(columns, row)) for row in c.fetchall()]
    conn.close()
    return {"shipments": shipments}

@app.get("/shipments/{shipment_id}")
async def get_shipment(shipment_id: int):
    conn = sqlite3.connect('shipments.db')
    c = conn.cursor()
    c.execute("SELECT * FROM shipments WHERE id = ?", (shipment_id,))
    columns = [description[0] for description in c.description]
    shipment = c.fetchone()
    conn.close()
    
    if shipment is None:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return {"shipment": dict(zip(columns, shipment))}