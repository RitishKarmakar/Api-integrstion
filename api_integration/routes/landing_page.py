from flask import Blueprint, jsonify, render_template,request
import requests
landing_bp = Blueprint("landing", __name__)

@landing_bp.route('/generate', methods=['POST'])
def generate_landing_page():
    data = request.json
    title = data.get('title', 'Default Title')
    description = data.get('description', 'Default Description')
    return render_template('landing_page.html', title=title, description=description)
