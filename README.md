# 📚 Collaborative Text Editor

Real-time collaborative text editor with multiple clients and live sync using WebSockets. 



### ✨ Features

- **Real-Time Collaboration** — instantly sync edits between users.

- **Session Management** — unique collaboration sessions via URL.

- **Operational Transformation (OT)** — safe concurrent editing without conflicts.

- **Undo Support** — each client can undo their last operation.

- **Network Delay Simulation** — introduce artificial lag to test synchronization.

- **Edit History** — request and replay full edit history.

- **Nginx Reverse Proxy** — production-ready HTTP routing and WebSocket support.


### 🛠 Tech Stack

**Backend**: Flask, Flask-SocketIO, Python

**Realtime Communication**: WebSockets via Socket.IO

**Frontend**: Vanilla JS + Socket.IO client

**Database**: MongoDB

**Web Server**: Nginx (reverse proxy for Flask-SocketIO)


### 📥 Installation

#### 1. Clone repository
```
git clone https://github.com/1sarmatt/sna_project.git
cd sna_project
```

#### 2. Install dependencies
```
pip install -r requirements.txt
```

#### 3. Run the server
```
python server/app.py
```

By default the app is listen on ```http://127.0.0.1:5001```

### 🌐 Nginx Configuration

**nginx.conf**:
```
worker_processes 1;

events {
    worker_connections 1024;
}

http {
    include       mime.types;
    default_type  application/octet-stream;

    sendfile        on;
    keepalive_timeout  65;

    server {
        listen       80;
        server_name  localhost;

        location / {
            proxy_pass         http://127.0.0.1:5001;
            proxy_http_version 1.1;
            proxy_set_header   Upgrade $http_upgrade;
            proxy_set_header   Connection "upgrade";
            proxy_set_header   Host $host;
        }
    }
}
```
Save it as ```/etc/nginx/nginx.conf```

And restart nginx: ```sudo systemctl restart nginx```

Now your app will be accessible via ```http://localhost/```

### 🚀 Usage

#### 1. Start or join a session
Start or join a session using UI.

#### 2. Editing
Text edits auto-sync across all connected clients.

#### 3. Undo last operation
Click the **Undo** button (or press Ctrl+Z) to revert the most recent change.

#### 4. Network delay simulation
Use the built-in delay slider in the UI to introduce artificial latency and test conflict resolution.

#### 5. Show history
Click the **Show History** button to view all operations.
