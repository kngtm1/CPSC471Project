from flask import Flask

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'something_secure'

    from .customer import customer
    from .auth import auth
    from .business import business
    from .frontPage import frontPage
    from .admin import admin

    app.register_blueprint(customer, url_prefix='/customer')
    app.register_blueprint(auth, url_prefix='/authenticate')
    app.register_blueprint(business, url_prefix='/business')
    app.register_blueprint(frontPage, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/admin')


    return app

