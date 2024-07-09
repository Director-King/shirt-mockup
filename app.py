from flask import Flask, render_template, request, redirect, url_for, flash
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

MAX_WIDTH = 105
MAX_HEIGHT = 72

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('upload_file'))
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def resize_image(image, max_width, max_height):
    width, height = image.size
    aspect_ratio = width / height

    if width > max_width:
        width = max_width
        height = int(width / aspect_ratio)

    if height > max_height:
        height = max_height
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
            width = int(request.form['width'])
            height = int(request.form['height'])
            x = int(request.form['x'])
            y = int(request.form['y'])
            original_width = int(request.form['originalWidth'])
            original_height = int(request.form['originalHeight'])

            # Load the base image and the uploaded design
            base_image_path = os.path.join(app.root_path, 'static/base_image.png')
            base_image = Image.open(base_image_path).convert("RGBA")
            uploaded_design = Image.open(file_path).convert("RGBA")

            # Resize the uploaded design to fit within MAX_WIDTH x MAX_HEIGHT while maintaining aspect ratio
            uploaded_design = resize_image(uploaded_design, MAX_WIDTH, MAX_HEIGHT)
            
            # Create a new image with the same size as the base image
            combined_image = Image.new("RGBA", base_image.size)
            
            # Paste the base image
            combined_image.paste(base_image, (0, 0))
            
            # Paste the uploaded design at the specified position
            combined_image.paste(uploaded_design, (x, y), uploaded_design)

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

    return render_template('index.html', file_url=file_url, download_url=download_url)

if __name__ == "__main__":
    os.makedirs(os.path.join(app.root_path, app.config['UPLOAD_FOLDER']), exist_ok=True)
    app.run(debug=True)