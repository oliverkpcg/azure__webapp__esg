from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from utils import *
import base64, io
import matplotlib
matplotlib.use('Agg')  # Use the non-interactive backend

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

# Set your desired password
PASSWORD = 'salary1234'

# Generate the test data
df = generate_test_data(1000)

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/password', methods=['GET', 'POST'])
def password():
    if request.method == 'POST':
        entered_password = request.form.get('password')
        if entered_password == PASSWORD:
            session['authenticated'] = True
            return redirect(url_for('salary_bands'))
        else:
            return render_template('password.html', error="Incorrect password")
    
    return render_template('password.html')

@app.route('/salary-bands', methods=['GET', 'POST'])
def salary_bands():
    # Check if user is authenticated
    if not session.get('authenticated'):
        return redirect(url_for('password'))
    
    if request.method == 'POST':
        selected_items = request.json
        selected_items = {key: [value for value in values if value != 'on'] for key, values in selected_items.items()}

        print(selected_items)  # Print the selected values to the backend
        
        # Generate the plot (your function returns plt object)
        plt_obj = plot_salary_ranges_by(df, selected_items)  # This returns plt object
        
        # Save the plot to a BytesIO object
        img = io.BytesIO()
        plt_obj.savefig(img, format='png')
        img.seek(0)
        plt_obj.close()  # Close the plt object to free memory

        # Encode image to base64 string
        img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')

        # Return the base64 string of the image as JSON
        return jsonify({"status": "success", "image": img_base64})

    # Pass DataFrame column values to the template
    departments = df['department'].unique().tolist()
    sexes = df['sex'].unique().tolist()
    cities = df['city'].unique().tolist()

    return render_template('salary_bands.html', departments=departments, sexes=sexes, cities=cities)


if __name__ == '__main__':
    app.run(debug=True)
    
