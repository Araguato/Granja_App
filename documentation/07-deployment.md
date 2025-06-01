# Deployment Guide

## 8.1 System Requirements

### 8.1.1 Server Requirements
- **Operating System**: Ubuntu 20.04 LTS / Windows Server 2019+
- **CPU**: 4+ cores
- **RAM**: 8GB+ (16GB recommended for production)
- **Storage**: 100GB+ (SSD recommended)
- **Database**: PostgreSQL 13+
- **Web Server**: Nginx/Apache
- **Python**: 3.8+
- **Node.js**: 16+ (for frontend build)

### 8.1.2 Client Requirements
- **Windows Application**:
  - Windows 10/11 (64-bit)
  - 4GB RAM
  - 500MB free disk space
  - .NET 6.0 Runtime

- **Mobile Application**:
  - Android 8.0+ (API 26+)
  - 2GB+ RAM
  - 100MB free storage

## 8.2 Server Setup

### 8.2.1 Initial Server Configuration

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install required system packages
sudo apt install -y git python3-pip python3-venv nginx postgresql postgresql-contrib

# Configure firewall
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

### 8.2.2 Database Setup

```bash
# Switch to postgres user
sudo -u postgres psql

# Create database and user
CREATE DATABASE granja_db;
CREATE USER granja_user WITH PASSWORD 'secure_password';
ALTER ROLE granja_user SET client_encoding TO 'utf8';
ALTER ROLE granja_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE granja_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE granja_db TO granja_user;
\q
```

## 8.3 Application Deployment

### 8.3.1 Backend Setup

```bash
# Create project directory
mkdir -p /opt/granja
cd /opt/granja

# Clone repository
git clone https://github.com/yourusername/granja-management.git .

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements/production.txt

# Configure environment variables
cp .env.example .env
nano .env  # Update with your configuration

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Create superuser
python manage.py createsuperuser
```

### 8.3.2 Gunicorn Setup

```bash
# Install Gunicorn
pip install gunicorn

# Create Gunicorn service file
sudo nano /etc/systemd/system/gunicorn.service
```

```ini
[Unit]
Description=gunicorn daemon for Granja
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/opt/granja
ExecStart=/opt/granja/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/granja.sock granja.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
# Start and enable Gunicorn
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

### 8.3.3 Nginx Configuration

```bash
# Create Nginx config
sudo nano /etc/nginx/sites-available/granja
```

```nginx
server {
    listen 80;
    server_name your_domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /opt/granja;
    }

    location /media/ {
        root /opt/granja;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/granja.sock;
    }
}
```

```bash
# Enable the site
sudo ln -s /etc/nginx/sites-available/granja /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

## 8.4 Windows Application Deployment

### 8.4.1 Build Process

1. Open solution in Visual Studio 2022
2. Set build configuration to "Release"
3. Right-click solution → "Publish"
4. Configure publish profile:
   - Target: Folder
   - Configuration: Release | Any CPU
   - Target Framework: net6.0-windows
   - Deployment Mode: Self-contained
   - Target Runtime: win-x64
5. Publish to folder

### 8.4.2 Installation

1. Create installer using Inno Setup or similar
2. Include required dependencies (.NET 6.0 Desktop Runtime if not bundled)
3. Create desktop and start menu shortcuts
4. Set up auto-update mechanism

## 8.5 Mobile Application Deployment

### 8.5.1 Android Build

```bash
# Build release APK
flutter build apk --release

# Build app bundle
flutter build appbundle --release
```

### 8.5.2 iOS Build (Future)

```bash
# Build iOS app
flutter build ios --release

# Open in Xcode
open ios/Runner.xcworkspace
```

## 8.6 Configuration Management

### 8.6.1 Environment Variables

```env
# Django Settings
DEBUG=False
SECRET_KEY=your_secret_key
ALLOWED_HOSTS=.yourdomain.com,localhost,127.0.0.1

# Database
DB_NAME=granja_db
DB_USER=granja_user
DB_PASSWORD=secure_password
DB_HOST=localhost
DB_PORT=5432

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_email_password

# API
API_BASE_URL=https://api.yourdomain.com
API_KEY=your_api_key

# Mobile App
MOBILE_APP_VERSION=1.0.0
MIN_ANDROID_VERSION=26
MIN_IOS_VERSION=13.0
```

## 8.7 Backup and Recovery

### 8.7.1 Database Backups

```bash
# Create backup directory
mkdir -p /var/backups/granja/db

# Create backup script
sudo nano /usr/local/bin/backup_granja_db.sh
```

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/var/backups/granja/db"
DB_NAME="granja_db"
DB_USER="granja_user"

# Create backup
PGPASSWORD="your_db_password" pg_dump -U $DB_USER -h localhost $DB_NAME > $BACKUP_DIR/granja_$DATE.sql

# Compress backup
gzip $BACKUP_DIR/granja_$DATE.sql

# Delete backups older than 30 days
find $BACKUP_DIR -name "granja_*.sql.gz" -type f -mtime +30 -delete
```

```bash
# Make script executable
chmod +x /usr/local/bin/backup_granja_db.sh

# Add to crontab for daily backups
(crontab -l 2>/dev/null; echo "0 2 * * * /usr/local/bin/backup_granja_db.sh") | crontab -
```

### 8.7.2 Media Files Backup

```bash
# Add to backup script
MEDIA_DIR="/opt/granja/media"
BACKUP_DIR="/var/backups/granja/media"
mkdir -p $BACKUP_DIR

# Create tar archive
tar -czf $BACKUP_DIR/media_$DATE.tar.gz -C $(dirname $MEDIA_DIR) $(basename $MEDIA_DIR)

# Delete backups older than 30 days
find $BACKUP_DIR -name "media_*.tar.gz" -type f -mtime +30 -delete
```

## 8.8 Monitoring and Maintenance

### 8.8.1 Logging

```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/var/log/granja/debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

### 8.8.2 Monitoring Tools
- **Server**: Prometheus + Grafana
- **Application**: Sentry
- **Database**: pgAdmin
- **Uptime**: Uptime Kuma

## 8.9 Security Hardening

### 8.9.1 Server Security
```bash
# Update system regularly
sudo apt update && sudo apt upgrade -y

# Install security updates automatically
sudo apt install -y unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades

# Configure SSH security
sudo nano /etc/ssh/sshd_config
# Change default port
# Disable root login
# Use key-based authentication
```

### 8.9.2 Django Security
```python
# settings.py
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

## 8.10 Scaling

### 8.10.1 Vertical Scaling
- Upgrade server resources (CPU, RAM, Storage)
- Optimize database queries
- Implement caching

### 8.10.2 Horizontal Scaling
- Load balancing with multiple application servers
- Database replication
- CDN for static/media files

## 8.11 Troubleshooting

### 8.11.1 Common Issues

#### Database Connection Issues
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Check connection logs
sudo tail -f /var/log/postgresql/postgresql-13-main.log
```

#### Gunicorn Issues
```bash
# Check Gunicorn status
sudo systemctl status gunicorn

# Check Gunicorn logs
sudo journalctl -u gunicorn
```

#### Nginx Issues
```bash
# Check Nginx status
sudo systemctl status nginx

# Check Nginx error logs
sudo tail -f /var/log/nginx/error.log
```

## 8.12 Support

### 8.12.1 Getting Help
- Check logs in `/var/log/granja/`
- Review documentation
- Contact support@yourcompany.com

### 8.12.2 Emergency Contacts
- System Administrator: +1234567890
- Database Administrator: +1234567891
- Development Team: dev@yourcompany.com
