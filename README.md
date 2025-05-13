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

- **Docker Support** — ready-to-use containerized deployment.


### 🛠 Tech Stack

**Backend**: Flask, Flask-SocketIO, Python

**Realtime Communication**: WebSockets via Socket.IO

**Frontend**: Vanilla JS + Socket.IO client

**Database**: MongoDB

**Infrastructure**: Docker, Nginx


### 📥 Installation

#### 1. Clone repository
```
git clone https://github.com/1sarmatt/sna_project.git
cd sna_project
```

#### 2. Run the docker
```
docker-compose up --build 
```

By default the app is listen on ```http://localhost```

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
