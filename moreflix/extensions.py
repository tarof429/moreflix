# Initialize LoginManager "extension"

from flask_login import LoginManager

login_manager = LoginManager()
login_manager.login_view = 'auth_bp.login'