from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'change-me-in-production'


from . import views  
from .users.views import users_bp  
from .products.views import products_bp  

app.register_blueprint(users_bp)
app.register_blueprint(products_bp)
