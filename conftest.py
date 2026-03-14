import pytest
from app import app, db
from models import Product, Post, Admin, Contact

@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

@pytest.fixture
def runner():
    """Create a CLI runner for the Flask application."""
    return app.test_cli_runner()

@pytest.fixture
def init_db_with_data(client):
    """Initialize database with test data."""
    with app.app_context():
        # Create test products
        product = Product(
            name='Test Carabiners',
            description='Test carabiners for climbing',
            price=49.99,
            category='Carabiners',
            in_stock=True
        )
        db.session.add(product)
        
        # Create test post
        post = Post(
            title='Test Article',
            content='This is a test article about climbing'
        )
        db.session.add(post)
        
        # Create test admin
        admin = Admin(username='testadmin', password='testpass123')
        db.session.add(admin)
        
        db.session.commit()
        return client
