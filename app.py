from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
import stripe
import csv
from datetime import datetime
from bs4 import BeautifulSoup

app = Flask(__name__)

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'ritishinternships@gmail.com'
app.config['MAIL_PASSWORD'] = '..Internship@2025'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

# Configure Stripe
stripe.api_key = ""

# CSV file to store payment history
PAYMENT_HISTORY_FILE = 'payment_history.csv'

# Ensure CSV file exists
try:
    with open(PAYMENT_HISTORY_FILE, mode='x', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Email', 'Transaction ID', 'Amount', 'Status', 'Date'])
except FileExistsError:
    pass

@app.route('/')
def home():
    # Load payment history from CSV
    payment_history = []
    with open(PAYMENT_HISTORY_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        payment_history = [row for row in reader]
    
    return render_template('index.html', payment_history=payment_history)

@app.route('/process_payment', methods=['POST'])
def process_payment():
    email = request.form['email']
    card_number = request.form['cardNumber']
    card_holder = request.form['cardHolder']
    expiry_date = request.form['expiryDate']
    cvv = request.form['cvv']

    # Parse expiry date
    try:
        exp_month, exp_year = map(int, expiry_date.split('/'))
    except ValueError:
        return redirect(url_for('home'))

    # Process payment using Stripe
    try:
        token = stripe.Token.create(
            card={
                "number": card_number,
                "exp_month": exp_month,
                "exp_year": exp_year,
                "cvc": cvv,
            }
        )
        charge = stripe.Charge.create(
            amount=5000,  # Amount in cents (e.g., $50.00)
            currency="usd",
            source=token.id,
            description="Payment for services",
            receipt_email=email,
        )

        # Record successful payment
        record_payment(email, charge.id, charge.amount, 'Success')

        send_email(email, "Payment Successful", generate_email_body_success(email))
        return redirect(url_for('thank_you'))

    except stripe.error.CardError as e:
        # Record failed payment
        record_payment(email, 'N/A', 5000, 'Failed')

        send_email(email, "Payment Failed", generate_email_body_failure(email))
        return redirect(url_for('sorry'))

@app.route('/thank_you')
def thank_you():
    # Render thank_you.html, which will redirect to home after 7 seconds
    return render_template('thank_you.html')

@app.route('/sorry')
def sorry():
    # Render sorry.html, which will redirect to home after 7 seconds
    return render_template('sorry.html')

def record_payment(email, transaction_id, amount, status):
    with open(PAYMENT_HISTORY_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([email, transaction_id, amount, status, datetime.now().strftime('%Y-%m-%d %H:%M:%S')])

def generate_email_body_success(email):
    html = f"""
    <html>
    <body>
        <h1>Payment Successful</h1>
        <p>Dear {email},</p>
        <p>Thank you for your payment. Your transaction has been processed successfully.</p>
        <p>Best Regards,<br>Ritish Internships Team</p>
    </body>
    </html>
    """
    return BeautifulSoup(html, "html.parser").prettify()

def generate_email_body_failure(email):
    html = f"""
    <html>
    <body>
        <h1>Payment Failed</h1>
        <p>Dear {email},</p>
        <p>We regret to inform you that your payment could not be processed. Please try again or contact support.</p>
        <p>Best Regards,<br>Ritish Internships Team</p>
    </body>
    </html>
    """
    return BeautifulSoup(html, "html.parser").prettify()

def send_email(to, subject, body):
    try:
        msg = Message(subject, sender=app.config['MAIL_USERNAME'], recipients=[to])
        msg.html = body
        mail.send(msg)
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == '__main__':
    app.run(debug=True)
