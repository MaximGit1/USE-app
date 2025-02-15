# 📚 USE-app - Unified State Exam Assistant Platform 🚀

**Your All-in-One Solution for Mastering Informatics Exams!**  
*DEMO Version - Bridging the Gap Between Learning & Excellence*

---

## 🚨 The Problem & Our Solution

⚠️ **"The Era of Tutors is Ending!"** - With growing discussions about phasing out private tutors, students need empowered self-learning tools.  

✅ **USE-app Comes to Rescue!** A full-stack platform for solving standardized Informatics exam tasks using Python.  
- 🧠 **Learn**: Access curated task-solving methodologies  
- 💻 **Code**: Write solutions directly in-browser  
- ✅ **Validate**: Get instant feedback on your answers  
- 📈 **Track Progress**: Monitor your learning journey  

---

## ✨ Key Features

| Category        | Features                                                                 |
|-----------------|--------------------------------------------------------------------------|
| 📚 **Task Library** | Curated collection of official exam-style problems                       |
| 🐍 **Python Editor**| Built-in IDE with syntax highlighting & execution                        |
| ⚡ **Real-Time Check**| Instant answer validation via microservices                             |
| 📊 **Analytics**    | Visual progress tracking & performance reports                          |
| 🔒 **Security**     | JWT authentication & HTTPS encryption                                   |

---

## 🛠 Tech Stack

### 🔧 Backend Services
| Service         | Technologies                                                                 |
|-----------------|------------------------------------------------------------------------------|
| **Main Service** | FastAPI 🚀, FastStream (RabbitMQ Producer), Redis, Dishka (DI)              |
| **Run Service**  | FastStream (RabbitMQ Consumer), Redis

### 🎨 Frontend
- **Framework**: Vue 3
- **Styling**: Bootstrap 5 
- **Tools**: Axios, Vue Router  

### 🛠 Infrastructure
- **Orchestration**: Docker Compose 🐳  
- **Web Server**: Nginx (SSL termination + reverse proxy)  
- **Messaging**: RabbitMQ 🐇  
- **Caching**: Redis 🔥  

---

## 🚀 Getting Started

### 1. Clone Repository 📥
```bash
git clone https://github.com/MaximGit1/USE-app
cd USE-app
```

### 2. Generate SSL Certificates 🔐
```bash
mkdir -p config/nginx/certs
openssl req -x509 -newkey rsa:4096 \
-keyout config/nginx/certs/key.pem \
-out config/nginx/certs/cert.pem \
-days 365 -nodes
```

### 3. Configure Services ⚙️
Follow individual READMEs for service-specific configurations:
- 📁 main_service/README.md
- 📁 run_service/README.md
- 📁 frontend/README.md

### 4. Launch System 🚀
```bash
docker-compose up --build
```

**Access the app at:** https://127.0.0.1/

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. 🍴 Fork the repository

2. 🌿 Create a feature branch (git checkout -b feature/amazing-feature)

3. 💾 Commit your changes

4. ⬆️ Push to the branch (git push origin feature/amazing-feature)

5. 🔀 Open a Pull Request

