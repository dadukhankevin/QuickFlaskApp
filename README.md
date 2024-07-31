# Flask Authentication App Tutorial

This readme will guide you through setting up a basic Flask application with user authentication. We'll cover important concepts about Flask, templates, and SQL.

## Step 1: Set up the environment

1. Install MySQL:
   ```
   brew install mysql
   brew services start mysql
   mysql_secure_installation
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate
   ```

3. Install required packages:
   ```
   pip install -r requirements.txt
   ```

## Step 2: Set up the database

1. Log in to MySQL:
   ```
   mysql -u root -p
   ```

2. Create the database and user:
   ```sql
   CREATE DATABASE flask_app_db;
   USE flask_app_db;
   CREATE USER 'flask_user'@'localhost' IDENTIFIED BY '1234';
   GRANT ALL PRIVILEGES ON flask_app_db.* TO 'flask_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

## Step 3: Understanding the Flask Application Structure

Our Flask app consists of several files:

1. `main.py`: The core of our Flask application
2. Templates:
   - `base.html`: The base template that other templates extend
   - `home.html`: The home page
   - `login.html`: The login page
   - `register.html`: The registration page
   - `dashboard.html`: The user dashboard

### Key Concepts:

- **Flask**: A micro web framework for Python
- **Jinja2 Templates**: Flask's templating engine for dynamic HTML
- **SQLAlchemy**: An ORM (Object-Relational Mapping) for database operations
- **Flask-SQLAlchemy**: Flask extension for easy SQLAlchemy integration
- **Werkzeug**: Provides security features like password hashing

## Step 4: Exploring the Code

### main.py

This file sets up the Flask application, defines routes, and handles user authentication:

- We use `Flask-SQLAlchemy` to interact with our MySQL database
- The `User` model defines our database schema
- Routes are defined for home, register, login, dashboard, and logout
- We use `werkzeug.security` for password hashing

### Templates

- `base.html`: Contains the basic structure of our HTML, including navigation
- `home.html`, `login.html`, `register.html`: Extend `base.html` and provide specific content
- `dashboard.html`: Shows user-specific information and allows attribute updates

### Important Flask Concepts

1. **Routing**: `@app.route()` decorator maps URLs to functions
2. **Request Handling**: `request.method` and `request.form` for form data
3. **Sessions**: `session` object for maintaining user state
4. **Flash Messages**: `flash()` for user feedback
5. **Redirects**: `redirect()` and `url_for()` for navigation

## Step 5: Running the Application

1. Ensure your virtual environment is activated
2. Run the Flask application:
   ```
   python flask_app.py
   ```
3. Open a web browser and navigate to `http://localhost:5000`