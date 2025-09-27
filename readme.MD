# Hiro – AI-Powered Recruitment Web Application

## 📌 Project Description
Hiro is an **AI-powered recruitment web application** designed to simplify the hiring process. Recruiters can post jobs, review applicants, and leverage AI-based scoring to identify the best candidates faster. The platform offers modern dashboards, applicant profiles with resume previews, and insightful analytics — all in a responsive, user-friendly interface.


---

## ✨ Features
- Public landing page with value proposition
- Authentication (Email/Password + Google)
- Recruiter dashboard with stats and AI scoring
- Applicant profile view with resume preview & notes
- Job posting and applicant tracking
- Contact applicants directly from profile view
- Settings for profile and notifications
- Fully responsive (desktop, tablet, mobile)

---

## 🛠️ Tech Stack
- **Frontend:** React, Tailwind CSS  
- **Backend:** Django / Django REST Framework  
- **Database:** PostgreSQL  
- **Authentication:** Email/Password + Google OAuth  
- **AI:** Resume parsing & candidate scoring  

---

## ⚙️ Setup Instructions

### Client (Frontend)
```bash
cd client
npm install
npm run start
```

### Server (Backend)
```bash
cd server

# Create Virtual Environment

# (Windows)
python -m venv venv 
.\venv\Scripts\activate

# (UNIX/MacOS)
python3 -m venv venv
source venv/bin/activate

# Run Server
python manage.py runserver

```
