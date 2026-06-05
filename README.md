# SmartStock Pro

Inventory Management System built with:

- Frontend: Nuxt 4 + Vuetify + TailwindCSS
- Backend: Django + Django REST Framework
- Database: PostgreSQL
- Production Process Manager:
  - PM2 (Nuxt Frontend)
  - Gunicorn (Django Backend)

---

# Project Structure

```bash
SmartStockPro/
├── SmartStockPro-FE/   # Nuxt 4 Frontend
└── SmartStockPro-BE/   # Django Backend
```

---

# Development Setup

# 1. Clone Repository

```bash
git clone <your-repository-url>
cd SmartStockPro
```

---

# 2. Backend Setup (Django)

## Enter Backend Directory

```bash
cd QuickFix_BE
```

## Create Virtual Environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create `.env`

example:

```env
SECRET_KEY=wtwZK6q1f0D2cRqM8ledWANK0DQAhRjtHjVk2WUn9OP2IuYmCOAjXxKF0WpMpsyw
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,10.0.2.2
CORS=http://localhost:3000,http://127.0.0.1:3000
ACT_URL=http://127.0.0.1:3000

DB_NAME=quickfixpharma
DB_USER=postgres
DB_PASSWORD=qwertyui
DB_HOST=127.0.0.1
DB_PORT=5432
```

---

## PostgreSQL Database

Create database manually:

```sql
CREATE DATABASE quickfixpharma;
```

---

## Run Migration

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Seed DB

```bash
python manage.py seed_db.py
```

---

## Run Development Server

```bash
python manage.py runserver
```

Backend runs on:

```text
http://127.0.0.1:8000
```

---

# 3. Frontend Setup (Nuxt 4)

## Enter Frontend Directory

```bash
cd ../QuickFIx_FE
```

---

## Install Dependencies

```bash
npm install
```

---

## Configure Environment Variables

Create `.env`

example:

```env
NUXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000/api/bnsp/
NUXT_PUBLIC_ACT_URL=http://localhost:3000
```

makesure to configure runtime copnfig inside nuxt.config.ts for the env above runtime config should look like this:

```bash
  runtimeConfig: {
    public: {
      apiBaseUrl: "",
      actUrl: "",
    },
  },
```

---

## Run Development Server

```bash
npm run dev
```

Frontend runs on:

```text
http://localhost:3000
```

---

# Production Deployment

Recommended OS:

- Ubuntu 22.04 LTS

---

# 1. Install Required Packages

## System Packages

```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx redis-server -y
```

---

## Node.js

```bash
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt install -y nodejs
```

---

## PM2

```bash
sudo npm install -g pm2
```

---

# 2. Django Production Setup

## Enter Backend Directory

```bash
cd QuickFix_BE
```

---

## Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
pip install gunicorn
```

---

## Production Environment Variables

Create `.env`

```env
DEBUG=False

SECRET_KEY=your-production-secret-key

ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

DB_NAME=quickfixpharma
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432
```

---

## Collect Static Files

```bash
python manage.py collectstatic
```

---

## Run Migration

```bash
python manage.py migrate
```

---

## Start Gunicorn

```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

Replace `config` with your Django project name.

---

## Run Gunicorn as Service

Create service:

```bash
sudo nano /etc/systemd/system/gunicorn.service
```

Example:

```ini
[Unit]
Description=Gunicorn daemon
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/QuickFix/QuickFix_BE
ExecStart=/home/ubuntu/QuickFix/QuickFix_BE/.venv/bin/gunicorn config.wsgi:application --bind 127.0.0.1:8000

---

mak sure to get the correct directory

[Install]
WantedBy=multi-user.target
```

---

## Enable Gunicorn

```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

---

# 3. Nuxt 4 Production Setup

## Enter Frontend Directory

```bash
cd ../SQuickFix_FE
```

---

## Install Dependencies

```bash
npm install
```

---

## Build Application

```bash
npm run build
```

---

## Start Using PM2

```bash
pm2 start .output/server/index.mjs --name quickfix_fe
```

---

## Save PM2 Process

```bash
pm2 save
```

---

## Auto Start PM2 on Boot

```bash
pm2 startup
```

Run the generated command afterward.

---

# 4. NGINX Reverse Proxy

Create config:

```bash
sudo nano /etc/nginx/sites-available/quickfix
```

Example:

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;

        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';

        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location /api {
        proxy_pass http://127.0.0.1:8000;
    }

    location /static/ {
        alias /home/ubuntu/QuickFix/QuickFix_BE/staticfiles/;
    }

    location /media/ {
        alias /home/ubuntu/QuickFix/QuickFix_BE/media/;
    }
}
```

---

make sure to get the correct dir

---

## Enable Site

```bash
sudo ln -s /etc/nginx/sites-available/quickfix /etc/nginx/sites-enabled
```

---

## Test NGINX

```bash
sudo nginx -t
```

---

## Restart NGINX

```bash
sudo systemctl restart nginx
```

---

# HTTPS SSL (Let's Encrypt)

Install Certbot:

```bash
sudo apt install certbot python3-certbot-nginx -y
```

Generate SSL:

```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

---

# Useful Commands

## PM2

Check processes:

```bash
pm2 list
```

Logs:

```bash
pm2 logs
```

Restart frontend:

```bash
pm2 restart quickfix_fe
```

---

## Gunicorn

Restart backend:

```bash
sudo systemctl restart gunicorn
```

Status:

```bash
sudo systemctl status gunicorn
```

Logs:

```bash
journalctl -u gunicorn -f
```

---

# Default Ports

| Service        | Port |
| -------------- | ---- |
| Nuxt Frontend  | 3000 |
| Django Backend | 8000 |
| PostgreSQL     | 5432 |

---

# Tech Stack

| Layer           | Technology            |
| --------------- | --------------------- |
| Frontend        | Nuxt 4                |
| UI Framework    | Vuetify               |
| Styling         | TailwindCSS           |
| Backend         | Django REST Framework |
| Database        | PostgreSQL            |
| Process Manager | PM2                   |
| Python Server   | Gunicorn              |
| Reverse Proxy   | NGINX                 |
| Queue/Broker    | Redis + Celery        |

---

# Authors

QuickFix Development Team
