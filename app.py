from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, static_folder='static')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        # Retrieve form data
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        message = request.form.get('message')

        # Here, you can process the data, store it in a database, or perform any other necessary actions.

        # For now, let's just display a success message.
        success_message = "Registration successful!"

        return render_template('success.html', message=success_message)

@app.route('/payment')
def payment():
    # Your payment processing logic goes here
    # For now, we'll just render the payment.html template
    return render_template('payment.html')


if __name__ == '__main__':
    app.run(debug=True)
