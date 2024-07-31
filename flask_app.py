# Import necessary modules from Flask and other libraries
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize Flask app and configure it
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Used for session security
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flask_user:1234@localhost/flask_app_db'  # Database connection string
db = SQLAlchemy(app)  # Create SQLAlchemy database instance

# Define User model for database
class User(db.Model):
    """
    User model for the database.
    
    Attributes:
        id (int): Primary key for the user.
        username (str): Unique username for the user.
        password (str): Hashed password for the user.
        attribute_int (int): An integer attribute for the user.
        attribute_str (str): A string attribute for the user.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    attribute_int = db.Column(db.Integer, nullable=True, default=0)  # An integer attribute
    attribute_str = db.Column(db.String(100), nullable=True, default='')  # A string attribute

# Route for home page
@app.route('/')
def home():
    """
    Render the home page.

    Returns:
        str: Rendered HTML template for the home page.
    """
    return render_template('home.html')

# Route for user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle user registration.

    If the request method is POST, attempt to register a new user.
    If the request method is GET, render the registration form.

    Returns:
        str: Rendered HTML template or a redirect response.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists')
            return redirect(url_for('register'))
        
        # Create new user with hashed password
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful')
        return redirect(url_for('login'))
    
    return render_template('register.html')

# Route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle user login.

    If the request method is POST, attempt to log in the user.
    If the request method is GET, render the login form.

    Returns:
        str: Rendered HTML template or a redirect response.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Verify user credentials
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id  # Store user ID in session
            flash('Login successful')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

# Route for user dashboard
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    """
    Handle user dashboard.

    If the user is not logged in, redirect to login page.
    If the request method is POST, update user attributes.
    If the request method is GET, render the dashboard.

    Returns:
        str: Rendered HTML template or a redirect response.
    """
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    
    if request.method == 'POST':
        # Update user attributes
        attribute_int = request.form.get('attribute_int')
        attribute_str = request.form.get('attribute_str')
        
        if attribute_int:
            user.attribute_int = int(attribute_int)
        if attribute_str:
            user.attribute_str = attribute_str
        
        db.session.commit()
        flash('User attributes updated successfully')
        return redirect(url_for('dashboard'))
    
    return render_template('dashboard.html', username=user.username, user=user)

# Route for user logout
@app.route('/logout')
def logout():
    """
    Handle user logout.

    Remove the user ID from the session and redirect to the home page.

    Returns:
        redirect: Redirect response to the home page.
    """
    session.pop('user_id', None)  # Remove user ID from session
    flash('You have been logged out')
    return redirect(url_for('home'))

# Run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)  # Run app in debug mode