# Deployment Guide for Carved Rock Fitness

This guide covers various deployment options for the Carved Rock Fitness Flask application.

## Table of Contents
1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Heroku](#heroku)
4. [AWS](#aws)
5. [DigitalOcean](#digitalocean)
6. [GitHub Pages (Static Deployment)](#github-pages-static-deployment)

## Local Development

### Quick Start
```bash
./setup.sh
source venv/bin/activate
flask run
```

Application runs at: `http://localhost:5000`

### Manual Setup
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -c "from app import app, init_db; init_db(app)"
flask run
```

## Docker Deployment

### Build Docker Image
```bash
docker build -t carved-rock-fitness .
```

### Run Docker Container
```bash
docker run -p 5000:5000 \
  -e SECRET_KEY="your-strong-secret-key" \
  -e FLASK_ENV=production \
  carved-rock-fitness
```

### Using Docker Compose (Development)
```bash
docker-compose up -d
```

Access at: `http://localhost:5000`

## Heroku

### Prerequisites
- Heroku CLI installed
- Heroku account

### Deploy Steps

1. **Create Procfile**
   ```
   web: gunicorn app:app
   ```

2. **Create runtime.txt** (optional, specifies Python version)
   ```
   python-3.11.4
   ```

3. **Initialize Heroku app**
   ```bash
   heroku login
   heroku create carved-rock-fitness
   ```

4. **Set environment variables**
   ```bash
   heroku config:set SECRET_KEY="your-strong-secret-key"
   heroku config:set FLASK_ENV=production
   ```

5. **Deploy**
   ```bash
   git push heroku main
   ```

6. **View logs**
   ```bash
   heroku logs --tail
   ```

### Heroku with PostgreSQL (Recommended for Production)
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

Update DATABASE_URL in .env:
```
DATABASE_URL=postgresql://...
```

## AWS (EC2 + RDS)

### EC2 Instance Setup

1. **Launch EC2 Instance**
   - AMI: Ubuntu 22.04 LTS
   - Instance Type: t3.micro (free tier)
   - Security Group: Allow port 80, 443, 22

2. **SSH into instance**
   ```bash
   ssh -i your-key.pem ubuntu@your-instance-ip
   ```

3. **Install dependencies**
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv nginx git -y
   ```

4. **Clone repository**
   ```bash
   git clone https://github.com/yourusername/carved-rock-website.git
   cd carved-rock-website
   ```

5. **Setup virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

6. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with production values
   nano .env
   ```

7. **Setup systemd service** (create `/etc/systemd/system/carved-rock.service`)
   ```
   [Unit]
   Description=Carved Rock Flask Application
   After=network.target

   [Service]
   User=ubuntu
   WorkingDirectory=/home/ubuntu/carved-rock-website
   ExecStart=/home/ubuntu/carved-rock-website/venv/bin/gunicorn --bind 127.0.0.1:5000 app:app
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

8. **Enable and start service**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable carved-rock
   sudo systemctl start carved-rock
   ```

9. **Configure Nginx** (create `/etc/nginx/sites-available/carved-rock`)
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

10. **Enable Nginx configuration**
    ```bash
    sudo ln -s /etc/nginx/sites-available/carved-rock /etc/nginx/sites-enabled/
    sudo nginx -t
    sudo systemctl restart nginx
    ```

11. **Setup SSL with Let's Encrypt**
    ```bash
    sudo apt install certbot python3-certbot-nginx -y
    sudo certbot --nginx -d your-domain.com
    ```

### RDS Database (PostgreSQL)
```bash
# AWS CLI command to create RDS instance
aws rds create-db-instance \
    --db-instance-identifier carved-rock-db \
    --db-instance-class db.t3.micro \
    --engine postgres \
    --master-username admin \
    --master-user-password your-password \
    --allocated-storage 20
```

## DigitalOcean

### App Platform (Recommended - Easiest)

1. **Connect GitHub repository** to DigitalOcean
2. **Configure App Spec** (auto-detected from Dockerfile)
3. **Set environment variables** in DigitalOcean console
4. **Deploy** - DigitalOcean handles everything

### Droplet Deployment (Manual)

1. **Create Droplet**
   - Ubuntu 22.04 LTS
   - Basic plan ($4-6/month)

2. **Follow AWS EC2 Setup Steps** (same as above)

3. **Use DigitalOcean Managed Database** (PostgreSQL)

## GitHub Pages (Static Deployment)

Note: GitHub Pages is for static sites. For dynamic Flask app, use one of the above options.

However, you can create a static export:
```bash
# Export Flask app routes to static HTML
python export_static.py
```

Then deploy `dist/` folder to GitHub Pages.

## Environment Variables for Production

```bash
export FLASK_ENV=production
export FLASK_DEBUG=False
export SECRET_KEY="your-strong-secret-key-min-32-chars"
export DATABASE_URL="postgresql://user:pass@host:port/dbname"
export FLASK_APP=app.py
export ADMIN_USERNAME="admin"
export ADMIN_PASSWORD="strong-password-change-me"
```

## SSL/TLS Certificates

### Let's Encrypt (Free)
```bash
certbot certonly --standalone -d your-domain.com
```

### Self-Signed (Testing Only)
```bash
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

## Database Backup

### SQLite
```bash
cp instance/carved_rock.db backups/carved_rock_$(date +%Y%m%d).db
```

### PostgreSQL
```bash
pg_dump DATABASE_NAME > backup_$(date +%Y%m%d).sql
```

## Monitoring and Logs

### Check Application Status (Systemd)
```bash
systemctl status carved-rock
journalctl -u carved-rock -f
```

### Gunicorn Logs
```bash
tail -f /var/log/gunicorn/access.log
tail -f /var/log/gunicorn/error.log
```

## Troubleshooting Deployments

### Issue: 502 Bad Gateway
- Check if Flask app is running: `systemctl status carved-rock`
- Check Nginx logs: `tail -f /var/log/nginx/error.log`
- Verify Nginx config: `nginx -t`

### Issue: Static Files Not Loading
- Ensure `static/` directory exists in deployment
- Configure Nginx to serve static files:
  ```nginx
  location /static/ {
      alias /path/to/carved-rock-website/static/;
  }
  ```

### Issue: Database Connection Error
- Verify DATABASE_URL is set correctly
- Check database credentials
- Ensure database server is running

### Issue: Secret Key Not Set
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## Performance Optimization

### Gunicorn Workers Calculation
```
workers = (2 × CPU cores) + 1
# For 2 cores: workers = 5
```

### Enable Caching
```nginx
add_header Cache-Control "public, max-age=3600";
```

### Database Connection Pooling
```python
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "pool_size": 10,
    "pool_recycle": 3600,
}
```

## Continuous Deployment

### GitHub Actions + Docker Hub
1. Push to `main` branch
2. GitHub Actions builds Docker image
3. Image pushed to Docker Hub
4. Deploy service pulls and runs latest image

See `.github/workflows/flask-ci.yml` for configuration.

---

**For additional help:**
- Check README.md for project overview
- Review app.py for code structure
- Check logs for error messages
