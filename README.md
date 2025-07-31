# ☁️ Cloud Resume Challenge - Sonali Mandrupkar

This is a cloud-based resume project inspired by the [Cloud Resume Challenge](https://cloudresumechallenge.dev). 
It highlights my skills in cloud computing, automation, and full-stack development by combining a static website frontend with a Python FastAPI backend—both deployed on Microsoft Azure.

# 🔍 Features

- Live visitor counter using Azure Table Storage
- Resume download functionality from Azure Blob Storage
- Frontend hosted via Azure Static Web Apps (Blob Storage `$web`)
- Backend API built with FastAPI and deployed to Azure App Service
- CI/CD pipelines using GitHub Actions

# 📊 Architecture Diagram

User
│
▼
Browser (Frontend: HTML/CSS/JS)
 │
 ├──> Fetch Visitor Count (/api/visitor)
 │          │
 │          ▼
 │    Azure Table Storage
 │
 └──> Download Resume (/api/resume)
            │
            ▼
      Azure Blob Storage
            ▲
            │
        FastAPI Backend (Azure App Service)


# ⚙️ Tech Stack

Frontend
- HTML5, CSS3, JavaScript (ES6+)
- Jest (Unit testing)
- Hosted on Azure Static Web Apps

Backend
- Python 3.10 with FastAPI
- Azure Blob Storage & Azure Table Storage
- Deployed via Azure App Service

DevOps
- GitHub Actions for CI/CD
- Azure Service Principal authentication
- Environment variables managed via Azure settings

# 🚀 Deployment

Frontend (via GitHub Actions)
- Automatically builds and deploys to Azure Blob `$web` storage when pushed to `main`.

Backend (via GitHub Actions)
- Installs dependencies, runs tests, and deploys to Azure App Service using a publish profile.

# 🧪 Testing

Frontend

- cd frontend
- npm install
- npm test

Backend

- cd backend
- pip install -r requirements.txt
- pytest

# 📬 Contact
Sonali Mandrupkar
- 📧 Email    : sonali.mandrupkar@gmail.com
- 🔗 LinkedIn : https://www.linkedin.com/in/sonali-mandrupkar-76bb4129/
- 💻 GitHub   : https://github.com/RareSonal/

# 📝 Acknowledgements

- Inspired by the Cloud Resume Challenge
- Website template based on CeeVee by StyleShout






