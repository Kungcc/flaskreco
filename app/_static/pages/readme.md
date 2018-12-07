
# Clean Flask Instance

## Flask Environment

### requirements
- Flask==1.0.2
- Flask-Admin==1.5.2
- Flask-Bootstrap==3.3.7.1
- Flask-SQLAlchemy==2.3.2
- Flask-Migrate==2.3.0 
- Flask-FlatPages==0.7.0
- gunicorn==19.9.0

### virtualenv
```
virtualenv env
source env/bin/activate
python36 -m pip install -r requirements.txt
```

### DB init & migration
```
python -m flask db init
python -m flask db migrate
python -m flask db upgrade
```

### run app
```
# debug mode
python -m flask run

# production mode
python .\wsgi.py
```

### flask shell
```
python -m flask shell
```

### Config.py & app/__init__.py
- app.config.from_object(DevConfig)
- app.config['LOG_TO_FILE'] = False
- [intergrated with Bootswatch theme](https://bootswatch.com/)
    - app.config['THEME'] = 'cerulean'
- flask-shell: `root/__init__.py`
- flask-admin
    - url: `/admin`
    - app.config['ADMIN'] = True
- flask-markdown
    - jinja: `{{ content | markdown}}`
- flask-flatpages
    - url: `/<file_name>`
    - app.main
    - page folder: `_static/pages`
    - page template folder: `_template/main/flatpages.html`

```
## for flask shell
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Todo': Todo}
```

<hr>

## File Structure

```
flaskc
├── app
│   ├── _static
│   │   ├── css >> styles.css: customize css style
│   │   ├── pages: static pages (.html/.md)
│   │
│   ├── _template
│   │   ├── _sub
│   │   │   ├── nav.html: menu setting
│   │   │   ├── footer.html: footer information
│   │   │   
│   │   ├── <app_name>
│   │
│   ├── <app_name>: view models
│   ├
│   ├── __init__.py: BluePrint route settings
│   ├── models.py: dbSchema settings    
│
├── src: *.db
└── lib: *.py
```

## New Instance

1. APP template: folder `app/main` as <app_name> folder
2. replace app name
    - `__init__.py`: line 3, 8
    - `route.py`: line 2 & add view functions
3. template: create <app_name> folder under `_template\<app_name>`
4. register blueprint urls under `app/__init__.py >> blueprint registration` section

```
# views
from app.main import bp as main_bp
app.register_blueprint(main_bp, url_prefix='/')
```

## Deployment
- [Install Nginx](https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-centos-7)
- [Serve Flask Applications](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04)

### Nginx
- `sudo nginx -s reload`

```nginx
#/etc/nginx/nginx.conf
# location /<blueprint_prefix>

location / {
    proxy_http_version 1.1;
    client_max_body_size 8m;    
    proxy_set_header Host $http_host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
	proxy_pass http://unix:/home/usr/flaskc/flaskc.sock;
}
```

### gunicorn
- `sudo systemctl start flaskc.service`

```systemctl 
#/etc/systemd/system/flaskc.service

[Unit]
Description=Gunicorn instance to serve flaskc
After=network.target

[Service]
WorkingDirectory=/home/usr/flaskc
Environment="PATH=/home/usr/flaskc/env/bin"
ExecStart=/home/usr/flaskc/env/bin/gunicorn --workers 3 --bind unix:flaskc.sock -m 007 wsgi:app

[Install]
WantedBy=multi-user.target

```