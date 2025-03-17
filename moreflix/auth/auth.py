from flask import Blueprint
from flask import render_template, request, session, redirect, url_for, flash 
from flask_login import login_user, logout_user
from moreflix.models import get_user

auth_bp = Blueprint('auth_bp', __name__,
    static_folder='static',
    template_folder='templates')

@auth_bp.route('/login', methods=["GET", "POST"])
def login():
    
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        user = get_user(username)
        
        if user and user.password == password:
            login_user(user)
            session['logged in'] = True
            session['username'] = username
            flash("Login successful!", "success")
            return redirect(url_for('movies_bp.index'))
        
        flash("Invalid credentials", "danger")
    return render_template("login.html")

@auth_bp.route('/signup')
def signup():
    return 'Signup'

@auth_bp.route('/logout')
def logout():
    logout_user()
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('welcome_bp.index'))