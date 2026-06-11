# Nginx Deployment Pitfalls

## Permission denied (13) serving from /home/ubuntu/

**The problem:** Nginx runs as `www-data` and cannot read files under `/home/ubuntu/` by default. Any `location` block pointing an `alias` or `root` to a path under `/home/ubuntu/` will produce 500 errors with `stat() failed (13: Permission denied)` in `/var/log/nginx/error.log`.

**The fix:** Copy static files to a web-root under `/var/www/` and use that path instead:

```bash
sudo mkdir -p /var/www/kb
sudo cp -r ~/oracle-kb/static/* /var/www/kb/
sudo chown -R www-data:www-data /var/www/kb
```

Then in the Nginx config:
```nginx
location /kb/ {
    alias /var/www/kb/;
    try_files $uri $uri/ /kb/index.html;
}
```

Do NOT use `root` when `location` matches a path prefix -- use `alias`. With `root`, Nginx appends the location path to the root (e.g. `root /var/www/kb` + `location /kb/` tries `/var/www/kb/kb/index.html`).

## Proxy pass to FastAPI/uvicorn

When proxying API calls to a local backend:

```nginx
location /api/ {
    proxy_pass http://127.0.0.1:8010/api/;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_read_timeout 120s;
}
```

The trailing slash on both `location /api/` and `proxy_pass .../api/` is important for correct path stripping.

## Systemd service for FastAPI

The service file lives at `/etc/systemd/system/oracle-kb.service`:

```ini
[Unit]
Description=Oracle KB FastAPI Server
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/oracle-kb
Environment=ORACLE_KB_PORT=8010
ExecStart=/home/ubuntu/.hermes/hermes-agent/venv/bin/python /home/ubuntu/oracle-kb/server.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Commands:
- `sudo systemctl start|stop|restart oracle-kb.service`
- `sudo systemctl enable oracle-kb.service` (auto-start on boot)
- `sudo journalctl -u oracle-kb.service -f` (tail logs)