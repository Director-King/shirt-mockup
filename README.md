README
This Flask web application allows users to upload their designs (PNG format), position them on a base image, and download the resulting mockup.

Features:

Secure Login: User authentication to protect uploads and processed designs.
Image Uploading: Upload PNG design files.
Positioning: Specify the exact position (x, y coordinates in inches) of the design on the base image.
Resizing: Automatic resizing of the design to fit within the base image dimensions while maintaining aspect ratio.
Preview: Real-time preview of the positioned and resized design.
Download: Download the full-sized mockup in PNG format.

How to Use:

Installation:
Clone the repository.
Install the required dependencies using pip install -r requirements.txt.
Set up your Flask environment variables (e.g., FLASK_APP, SECRET_KEY).

Running the App:
Start the Flask development server: flask run.
Open your web browser and navigate to http://127.0.0.1:5000/.

Login:
The basic version automatically logs you in.
If you found yourself log out enter "user1" and "password1" to log in.

Uploading and Processing:
Click "Choose a PNG file" and select your design.
There is deault data input when ou upload your design but you can customize you own measurments just enter the desired width, height, x position, and y position in inches.
Click "Upload and Process."
The app will display a preview of the processed design.

Downloading:
Click "Download Full Size" to download the high-resolution mockup.

Code Structure:

app.txt: Contains the main Flask application logic, including routing, image processing, and user authentication.
index.txt: The HTML template for the main page (upload and processing).
login.txt: The HTML template for the login page.
script.txt: Client-side JavaScript for image previews, input validation, and unit conversion.
_navbar.txt: HTML for the navigation bar (included in other templates).
static/: Directory for CSS stylesheets, JavaScript files, and uploaded images.

Dependencies:

Flask
Pillow (PIL)
Flask-Login (for user authentication)

Additional Notes:

This is a basic implementation. Consider adding more features and security measures for a production environment.
The provided user accounts are placeholders. In a real application, you would typically use a database to store user information.
Ensure that you have the necessary image processing libraries (e.g., Pillow) installed.
