import pytest
from app import app, db
from models import Product, Post, Admin

def test_index_route(client):
    """Test homepage loads successfully."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Carved Rock' in response.data

def test_products_route(client, init_db_with_data):
    """Test products page loads."""
    response = client.get('/products')
    assert response.status_code == 200

def test_articles_route(client, init_db_with_data):
    """Test articles page loads."""
    response = client.get('/articles')
    assert response.status_code == 200

def test_about_route(client):
    """Test about page loads."""
    response = client.get('/about')
    assert response.status_code == 200

def test_contact_get(client):
    """Test contact form loads."""
    response = client.get('/contact')
    assert response.status_code == 200

def test_contact_post(client):
    """Test contact form submission."""
    response = client.post('/contact', data={
        'name': 'Test User',
        'email': 'test@example.com',
        'message': 'Test message'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Thank you' in response.data

def test_admin_login_get(client):
    """Test admin login page loads."""
    response = client.get('/admin/login')
    assert response.status_code == 200

def test_404_error(client):
    """Test 404 error page."""
    response = client.get('/nonexistent-page')
    assert response.status_code == 404

def test_product_detail(client, init_db_with_data):
    """Test product detail page."""
    response = client.get('/product/1')
    assert response.status_code == 200

def test_article_detail(client, init_db_with_data):
    """Test article detail page."""
    response = client.get('/article/1')
    assert response.status_code == 200
