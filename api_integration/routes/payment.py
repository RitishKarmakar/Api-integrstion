from flask import Blueprint, jsonify, request
from utils.payment import process_payment

payment_bp = Blueprint("payment", __name__)

@payment_bp.route('/process', methods=['POST'])
def process():
    data = request.json
    result = process_payment(data)
    return jsonify(result)
