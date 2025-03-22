import streamlit as st
import requests
import json

BASE_URL = "http://localhost:8000"

def create_shipment():
    st.subheader("Create New Shipment")
    
    with st.form("shipping_form"):
        product_name = st.text_input("Product Name")
        quantity = st.number_input("Quantity", min_value=1, step=1)
        destination = st.text_input("Destination")
        customer_name = st.text_input("Customer Name")
        priority = st.selectbox("Priority", ["normal", "urgent"])
        
        submitted = st.form_submit_button("Create Shipment")
        
        if submitted:
            if not all([product_name, destination, customer_name]):
                st.error("Please fill in all required fields")
                return
                
            payload = {
                "product_name": product_name,
                "quantity": quantity,
                "destination": destination,
                "customer_name": customer_name,
                "priority": priority
            }
            
            try:
                response = requests.post(f"{BASE_URL}/shipments/", json=payload)
                response.raise_for_status() 
                st.success("Shipment created successfully!")
                st.json(response.json())
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to create shipment: {str(e)}")

def view_shipments():
    st.subheader("View Shipments")
    
    try:
        response = requests.get(f"{BASE_URL}/shipments/")
        response.raise_for_status()
        shipments = response.json()["shipments"]
        if not shipments:
            st.write("No shipments found")
        else:
            for shipment in shipments:
                st.write(f"Shipment #{shipment['id']}")
                st.write(f"Product: {shipment['product_name']}")
                st.write(f"Quantity: {shipment['quantity']}")
                st.write(f"Destination: {shipment['destination']}")
                st.write(f"Customer: {shipment['customer_name']}")
                st.write(f"Priority: {shipment['priority']}")
                st.write(f"Status: {shipment['status']}")
                st.write(f"Created: {shipment['created_at']}")
                st.write("---")
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch shipments: {str(e)}")

def main():
    st.title("Shipping Management System")
    
    menu = ["Create Shipment", "View Shipments"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Create Shipment":
        create_shipment()
    elif choice == "View Shipments":
        view_shipments()

if __name__ == "__main__":
    main()