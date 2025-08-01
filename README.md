## OpenBild

**OpenBild** is a developer collaboration platform where developers can sign up (via email/password or GitHub OAuth), post their projects, explore other developers' projects, and send collaboration requests. When a developer shows interest in a project, they can drop a message to the project owner, which triggers an email notification for seamless connection and collaboration.

---

### 🚧 Status
> This project is in its initial setup phase. Core features and documentation will be updated iteratively.

---

### 🚀 Planned Features

- **User Authentication**
  - Email/password registration & login (JWT-based).
  - Social login with **GitHub OAuth**.
- **Developer Profiles**
  - Editable bio, skills/tags, GitHub profile link, and avatar upload.
- **Project Posting**
  - Create, edit, delete, and manage projects.
  - Include title, description, tech stack tags, repo URL, and thumbnail image.
- **Explore Projects**
  - Browse public projects, filter by tech stack or tags, and search by keywords.
- **Collaboration Requests**
  - Send collaboration messages to project owners.
  - Automatic email notifications to project owners upon requests.
- **Notifications**
  - In-app notifications for new collaboration requests and activity updates.
- **Dashboard**
  - Centralized area to view active projects, collaboration requests, and notifications.

---

### 🛠 Tech Stack

**Backend:**
- Django + Django REST Framework (DRF)
- PostgreSQL (database)
- JWT Authentication (`djangorestframework-simplejwt`)
- GitHub OAuth (`django-allauth` + `dj-rest-auth`)
- Django Filters & Pagination
- Email notifications (SMTP)

**Frontend:**
- React (Vite)
- React Router for navigation
- Axios for API integration
- Tailwind CSS (UI styling)

**Other:**
- GitHub OAuth App (for login integration)

---

### 🏗 Getting Started (WIP)
Setup instructions will be added as the project progresses.

---

### 📜 License
This project will be licensed under the MIT License (to be added).
