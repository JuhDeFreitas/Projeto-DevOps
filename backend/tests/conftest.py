import pytest
from flask import Flask

from database import db
from routes import api


# =========================
# FIXTURE - APP DE TESTE
# =========================
@pytest.fixture
def app():
    app = Flask(__name__)

    # Configuração de teste
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    # Inicialização do banco e rotas
    db.init_app(app)
    app.register_blueprint(api)

    # Setup do banco
    with app.app_context():
        db.create_all()

    yield app

    # Teardown (limpeza)
    with app.app_context():
        db.session.remove()
        db.drop_all()


# =========================
# FIXTURE - CLIENTE TESTE
# =========================
@pytest.fixture
def client(app):
    return app.test_client()