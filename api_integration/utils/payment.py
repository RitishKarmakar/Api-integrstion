def process_payment(data):
    # Mock payment processing logic
    amount = data.get("amount")
    payment_method = data.get("payment_method")
    return {"status": "success", "message": f"Processed ${amount} via {payment_method}"}
