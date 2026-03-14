# Carved Rock Fitness - E-commerce Application

A modern, full-featured e-commerce web application for rock climbing and fitness equipment, built with Flask, SQLAlchemy, and Bootstrap 5.

## Features

- 🏔️ **Product Catalog** - Browse and search climbing equipment
- 📝 **Blog/Articles** - Read articles about climbing techniques and fitness
- 👤 **User Authentication** - Admin login system with session management
- 📊 **Admin Dashboard** - Manage products, articles, and customer messages
- 💬 **Contact Form** - Customers can send inquiries
- 📦 **Database** - SQLite with SQLAlchemy ORM
- 🎨 **Responsive Design** - Mobile-friendly Bootstrap 5 interface
- 🐳 **Docker Support** - Production-ready Dockerfile and docker-compose

## Tech Stack

- **Backend**: Flask 2.3.3, Flask-SQLAlchemy, Flask-Login
- **Frontend**: Bootstrap 5.3.0, Jinja2 Templates
- **Database**: SQLite3
- **Server**: Gunicorn WSGI server
- **Containerization**: Docker & Docker Compose

## Quick Start

### Prerequisites
- Python 3.11+
- pip
- Docker (optional, for containerized deployment)

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/carved-rock-website.git
   cd carved-rock-website
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create .env file** (copy from .env.example)
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run the application**
   ```bash
   flask run
   ```
   Application will be available at `http://localhost:5000`

6. **Access Admin Dashboard**
   - Navigate to `http://localhost:5000/admin/login`
   - Default credentials: `admin` / `changeme123` (change in production!)

### Docker Deployment

**Build and run with Docker Compose** (recommended for development):
```bash
docker-compose up -d
```

**Build Docker image for production**:
```bash
docker build -t carved-rock-fitness .
docker run -p 5000:5000 carved-rock-fitness
```

## Project Structure

```
├── app.py                      # Main Flask application
├── models.py                   # SQLAlchemy database models
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Production Docker image
├── docker-compose.yml          # Local development Docker Compose
├── .env.example                # Environment variables template
├── templates/                  # Jinja2 HTML templates
│   ├── base.html              # Base template with navbar
│   ├── index.html             # Homepage
│   ├── products.html          # Product listing
│   ├── product_detail.html    # Individual product view
│   ├── articles.html          # Articles listing
│   ├── article_detail.html    # Individual article view
│   ├── about.html             # About page
│   ├── contact.html           # Contact form
│   ├── admin_login.html       # Admin login
│   ├── admin_dashboard.html   # Admin control panel
│   ├── add_product.html       # Add product form
│   ├── add_post.html          # Add article form
│   ├── 404.html               # 404 error page
│   └── 500.html               # 500 error page
└── static/                     # Static files
    ├── css/
    │   └── style.css          # Custom styles
    ├── js/                     # JavaScript files
    └── images/                 # Product/article images
```

## Database Models

### Product
- id, name, description, price, category, image_url, in_stock

### Post
- id, title, content, image_url, created_at, updated_at

### Contact
- id, name, email, message, created_at

### Admin
- id, username, password_hash (hashed with Werkzeug)

## Configuration

Edit `.env` file to configure:
- `FLASK_ENV` - Set to "development" or "production"
- `SECRET_KEY` - Session secret (generate a strong one!)
- `DATABASE_URL` - SQLite database path
- `ADMIN_USERNAME` - Admin account username
- `ADMIN_PASSWORD` - Admin account password

## Key Routes

### Public Routes
- `/` - Homepage
- `/products` - Product catalog
- `/product/<id>` - Product detail
- `/articles` - Articles listing
- `/article/<id>` - Article detail
- `/about` - About page
- `/contact` - Contact form

### Admin Routes
- `/admin/login` - Admin login
- `/admin/logout` - Admin logout
- `/admin/dashboard` - Control panel (requires authentication)
- `/admin/product/add` - Add new product
- `/admin/product/<id>/delete` - Delete product
- `/admin/post/add` - Add new article
- `/admin/post/<id>/delete` - Delete article

## Environment Variables

```
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=False
SECRET_KEY=your-secret-key-change-this
DATABASE_URL=sqlite:///carved_rock.db
ADMIN_USERNAME=admin
ADMIN_PASSWORD=changeme123
```

## Development Features

- **Auto-reload** - Flask development server auto-reloads on code changes
- **Debug toolbar** - Available in development mode
- **Sample data** - Database initializes with sample products and articles
- **Error pages** - Custom 404 and 500 error pages

## Production Deployment

1. **Set strong SECRET_KEY** in environment
2. **Use production database** (PostgreSQL recommended over SQLite)
3. **Configure CSRF protection** in app.py
4. **Use reverse proxy** (nginx) with Gunicorn
5. **Enable HTTPS** (Let's Encrypt)
6. **Set DEBUG=False**

Example Gunicorn command:
```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 60 app:app
```

## Security Considerations

⚠️ **Important**: This is a base template. For production:
- Change default admin credentials immediately
- Use a strong SECRET_KEY
- Enable CSRF protection
- Validate and sanitize all user inputs
- Use environment variables for sensitive data
- Implement rate limiting
- Add email verification for contact forms
- Use HTTPS only

## Customization

### Add Custom Styling
Edit `static/css/style.css` to modify colors and styles.

### Add New Routes
Add new functions in `app.py` with `@app.route()` decorator:
```python
@app.route('/new-page')
def new_page():
    return render_template('new_page.html')
```

### Add New Database Models
Create model class in `models.py` and run `init_db()` to create tables.

## Troubleshooting

**Issue**: Database file not created
- Solution: Run the app once, it auto-creates on first run

**Issue**: Admin login fails
- Solution: Check `ADMIN_USERNAME` and `ADMIN_PASSWORD` in `.env`

**Issue**: Images not displaying
- Solution: Ensure images exist in `static/images/` directory

**Issue**: Port 5000 already in use
- Solution: Change port in `flask run --port 8000`

## Future Enhancements

- [ ] Shopping cart functionality
- [ ] Payment integration (Stripe/PayPal)
- [ ] Email notifications
- [ ] User registration and accounts
- [ ] Product reviews and ratings
- [ ] Search functionality
- [ ] Category filters
- [ ] Email newsletter
- [ ] Image upload instead of URL references

## License

MIT License - feel free to use this project for learning and development.

## Support

For issues, questions, or suggestions, please open a GitHub issue or contact the development team.

---

**Built with ❤️ by the Carved Rock Team**
