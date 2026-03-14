from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Product, Post, Contact, Admin
import os
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///carved_rock.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

def init_db(app):
    """Initialize database with sample data"""
    with app.app_context():
        db.create_all()
        
        # Check if data already exists
        if Product.query.first():
            return
        
        # Sample products
        products = [
            Product(name='Carabiners Pro', description='Professional carabiners for rock climbing', 
                   price=49.99, category='Carabiners', image_url='/static/images/carabiner.jpg', in_stock=True),
            Product(name='Ice Axes Bundle', description='Complete ice climbing axes set', 
                   price=199.99, category='Ice Axes', image_url='/static/images/ice-axe.jpg', in_stock=True),
            Product(name='Climbing Rope 50m', description='High-quality climbing rope 50 meters', 
                   price=89.99, category='Ropes', image_url='/static/images/rope.jpg', in_stock=True),
        ]
        
        # Sample posts
        posts = [
            Post(title='Carabiners for Diwali Sale', 
                content='Get 20% off on all carabiners this season. Professional grade equipment at unbeatable prices.',
                image_url='/static/images/carabiner.jpg'),
            Post(title='Ice Axes On Sale', 
                content='Premium ice climbing equipment now available. Perfect for winter climbing season.',
                image_url='/static/images/ice-axe.jpg'),
        ]
        
        for product in products:
            db.session.add(product)
        for post in posts:
            db.session.add(post)
        
        db.session.commit()

# Routes
@app.route('/')
def index():
    featured_posts = Post.query.order_by(Post.created_at.desc()).limit(2).all()
    featured_products = Product.query.filter_by(in_stock=True).limit(3).all()
    return render_template('index.html', posts=featured_posts, products=featured_products)

@app.route('/products')
def products():
    category = request.args.get('category', None)
    if category:
        products_list = Product.query.filter_by(category=category, in_stock=True).all()
    else:
        products_list = Product.query.filter_by(in_stock=True).all()
    
    categories = db.session.query(Product.category).distinct().all()
    categories = [cat[0] for cat in categories]
    return render_template('products.html', products=products_list, categories=categories, selected_category=category)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

@app.route('/articles')
def articles():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('articles.html', posts=posts)

@app.route('/article/<int:post_id>')
def article_detail(post_id):
    post = Post.query.get_or_404(post_id)
    related_posts = Post.query.filter(Post.id != post_id).order_by(Post.created_at.desc()).all()
    return render_template('article_detail.html', post=post, related_posts=related_posts)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        if name and email and message:
            contact_msg = Contact(name=name, email=email, message=message)
            db.session.add(contact_msg)
            db.session.commit()
            flash('Thank you! Your message has been sent.', 'success')
            return redirect(url_for('contact'))
        flash('Please fill in all fields.', 'error')
    
    return render_template('contact.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        admin = Admin.query.filter_by(username=username).first()
        
        if admin and check_password_hash(admin.password, password):
            login_user(admin)
            return redirect(url_for('admin_dashboard'))
        flash('Invalid credentials', 'error')
    
    return render_template('admin_login.html')

@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    products = Product.query.all()
    posts = Post.query.all()
    contacts = Contact.query.all()
    return render_template('admin_dashboard.html', products=products, posts=posts, contacts=contacts)

@app.route('/admin/product/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        product = Product(
            name=request.form.get('name'),
            description=request.form.get('description'),
            price=float(request.form.get('price')),
            category=request.form.get('category'),
            image_url=request.form.get('image_url', '/static/images/placeholder.jpg'),
            in_stock=request.form.get('in_stock') == 'on'
        )
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('add_product.html')

@app.route('/admin/product/delete/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/post/add', methods=['GET', 'POST'])
@login_required
def add_post():
    if request.method == 'POST':
        post = Post(
            title=request.form.get('title'),
            content=request.form.get('content'),
            image_url=request.form.get('image_url', '/static/images/placeholder.jpg')
        )
        db.session.add(post)
        db.session.commit()
        flash('Post added successfully', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('add_post.html')

@app.route('/admin/post/delete/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted', 'success')
    return redirect(url_for('admin_dashboard'))

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    init_db(app)
    app.run(debug=False, host='0.0.0.0', port=5000)
