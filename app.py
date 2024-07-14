from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os
from PIL import Image

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Change this to a random secret key
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png'}

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

BASE_IMAGES = {
    'dress-shirt': {
        'file': 'base_image.png',
        'max_width': 105,
        'max_height': 72,
        'default_x': 597.1,
        'default_y': 321.6
    },
    't-shirt': {
        'file': 't-shirt.png',
        'max_width': 27.3,
        'max_height': 19,
        'default_x': 201,
        'default_y': 105
    },
    'polo-shirt': {
        'file': 'polo-shirt.png',
        'max_width': 43.1,
        'max_height': 31.1,
        'default_x': 350,
        'default_y': 180
    }
}

# This is a simple user model. In a real application, you'd use a database.
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

# This is a simple user database. In a real application, you'd use a real database.
users = {
    'user1': User('1', 'user1', generate_password_hash('password1')),
    'user2': User('2', 'user2', generate_password_hash('password2'))
}

@login_manager.user_loader
def load_user(user_id):
    for user in users.values():
        if user.id == user_id:
            return user
    return None

#MAX_WIDTH = 105
#MAX_HEIGHT = 72

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('pricing_calculator'))
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/pricing', methods=['GET', 'POST'])
@login_required
def pricing_calculator():
    if request.method == 'POST':
        printing_type = request.form['printing_type']
        
        if printing_type == 'digital':
            size = request.form['size']
            sided = request.form['sided']
            paper_type = request.form['paper_type']
            copies = int(request.form['copies'])
            
            # Perform digital printing price calculation
            price = calculate_digital_price(size, sided, paper_type, copies)
            
            return jsonify({'price': price})
        
        elif printing_type == 'no_cut':
            cloth_type = request.form['cloth_type']
            quantity = int(request.form['quantity'])
            
            # Perform no-cut printing price calculation
            price = calculate_no_cut_price(cloth_type, quantity)
            
            return jsonify({'price': price})
    
    return render_template('pricing_calculator.html')

def calculate_digital_price(size, sided, paper_type, copies):
    # Implement the pricing logic based on the provided calculations
    # This is a simplified version, you'll need to expand it
    base_price = {
        'A6': 5 if sided == '1' else 9,
        'A5': 10 if sided == '1' else 19,
        'A4': 19 if sided == '1' else 38,
        'A3': 38 if sided == '1' else 75
    }
    
    if paper_type in ['Art/Matt 250gsm', 'Art/Matt 300gsm']:
        base_price = {k: v + 2 for k, v in base_price.items()}
    
    return base_price[size] * copies

def calculate_no_cut_price(cloth_type, quantity):
    base_price = 120
    if cloth_type == 'Corporate shirt':
        return (base_price + 1200) * quantity
    elif cloth_type == 'Round-neck shirt':
        return (base_price + 350) * quantity
    elif cloth_type == 'Polo-shirt':
        return (base_price + 450) * quantity

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def resize_image(image, max_width, max_height):
    width, height = image.size
    aspect_ratio = width / height

    if width > max_width:
        width = int(max_width)
        height = int(width / aspect_ratio)

    if height > max_height:
        height = int(max_height)
        width = int(height * aspect_ratio)

    return image.resize((width, height), Image.LANCZOS)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    file_url = None
    download_url = None
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Get dimensions and position from form
            width = float(request.form['width'])
            height = float(request.form['height'])
            x = float(request.form['x'])
            y = float(request.form['y'])
            base_image_key = request.form['base_image']
            base_image_info = BASE_IMAGES[base_image_key]

            # Load the base image and the uploaded design
            base_image_path = os.path.join(app.root_path, 'static', base_image_info['file'])
            base_image = Image.open(base_image_path).convert("RGBA")
            uploaded_design = Image.open(file_path).convert("RGBA")

            # Resize the uploaded design to fit within max_width x max_height while maintaining aspect ratio
            uploaded_design = resize_image(uploaded_design, base_image_info['max_width'], base_image_info['max_height'])
            
            # Create a new image with the same size as the base image
            combined_image = Image.new("RGBA", base_image.size)
            
            # Paste the base image
            combined_image.paste(base_image, (0, 0))
            
            # Paste the uploaded design at the specified position
            combined_image.paste(uploaded_design, (int(x), int(y)), uploaded_design)

            # Save full-size image for download
            full_size_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], 'full_' + filename)
            combined_image.save(full_size_path)

            # Create and save thumbnail for display
            thumbnail_size = (300, 300)
            thumbnail = combined_image.copy()
            thumbnail.thumbnail(thumbnail_size)
            thumbnail_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], 'thumb_' + filename)
            thumbnail.save(thumbnail_path)

            # Generate the URLs for the thumbnail and full-size image
            file_url = url_for('static', filename='uploads/' + 'thumb_' + filename)
            download_url = url_for('static', filename='uploads/' + 'full_' + filename)

    return render_template('index.html', file_url=file_url, download_url=download_url, base_images=BASE_IMAGES)

if __name__ == "__main__":
    os.makedirs(os.path.join(app.root_path, app.config['UPLOAD_FOLDER']), exist_ok=True)
    app.run(debug=True)