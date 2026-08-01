server {
    server_name report.envitechal.com www.report.envitechal.com;
    client_max_body_size 150M;

    # performance: compression
    gzip on;
    gzip_comp_level 5;
    gzip_min_length 256;
    gzip_proxied any;
    gzip_vary on;
    gzip_types text/plain text/css application/javascript application/json application/xml image/svg+xml font/woff font/woff2; 

    location = /favicon.ico { alias /home/django/EnviTechAlApp/staticfiles/assets/favicon.ico; access_log off; log_not_found off; expires 30d; }

    # collectstatic writes each asset with a hash of its contents in the name,
    # so a hashed file can never change. Cache those for a year; everything else
    # under /static/ keeps the ordinary policy below.
    location ~ "^/static/(.+\.[0-9a-f]{12}\.[A-Za-z0-9]+)$" {
        alias /home/django/EnviTechAlApp/staticfiles/$1;
        access_log off;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location /static/ {
        alias /home/django/EnviTechAlApp/staticfiles/;
        expires 30d;
        add_header Cache-Control public;
    }

    location /media/ {
        alias /home/django/EnviTechAlApp/media/;
        expires 7d;
        add_header Cache-Control public;
    }

    location / {
        proxy_pass http://unix:/run/gunicorn.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
	proxy_connect_timeout 7200;
	proxy_send_timeout 7200;
	proxy_read_timeout 7200;
	send_timeout 7200;
    }

    listen 443 ssl;
    ssl_certificate /etc/letsencrypt/live/report.envitechal.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/report.envitechal.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
}

server {
    if ($host = report.envitechal.com) {
        return 301 https://$host$request_uri;
    }

    listen 80;
    server_name report.envitechal.com www.report.envitechal.com;
    return 404;
}
