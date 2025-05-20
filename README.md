# 🏌️‍♂️ BGA League Tracker — Final Project (General Assembly)

This application is the **capstone project** of my Software Engineering program at General Assembly — and a long-term passion project designed to track the history, stats, and competitiveness of the **Beast Golf Association (BGA)**, a Minnesota-based tour of legendary 2-man scrambles and major tournaments.

I built it to showcase my full-stack development skills while creating something useful and meaningful for my community.

🔗 **Live Site:** [https://bgaapp.fly.dev/](https://bgaapp.fly.dev/)

---

## 🚀 Tech Stack

**Backend:**
- Python 3.11  
- Django 5.0  
- PostgreSQL (hosted via Fly.io)

**Frontend:**
- Django Templates (MVT)  
- Bootstrap 5  
- Custom CSS (`styles.css`)

**Deployment & DevOps:**
- Fly.io (Docker-based deployment)
- Git & GitHub
- Admin login & live database seeded via fixture

---

## 💡 Key Features

- Countdown and display of **next and most recent event** on the homepage
- Full **event management system**: create, edit, delete events + dynamic schedule view
- **Score submission** with player matching, placement calculation, and tie handling
- **Leaderboard medals** 🥇🥈🥉 based on dynamic sorting and placement logic
- **Auto-complete player name form** via `<datalist>`
- Tour player profiles showing **dynamic career stats** (events played, wins, majors)
- Legacy archive of **all BGA seasons**, dynamically grouped by year

---

## 🧠 What I Taught Myself

This project pushed me beyond the GA curriculum. I independently learned how to:

- ✅ Deploy a full Django app using **Fly.io**
- ✅ Provision and manage a **PostgreSQL production cluster**
- ✅ Load and sanitize **fixture data** inside Docker containers
- ✅ Secure the app with **CSRF protection**, domain trust settings, and secret keys
- ✅ Build **calculated fields** in models (e.g., career wins, events played) using `@property`
- ✅ Recalculate **placement logic with tie detection** across leaderboard events
- ✅ Implement **finalization logic** to control when results affect career stats

---

## 🔒 Admin Panel (Live)

Access the admin backend (requires login):

👉 [https://bgaapp.fly.dev/admin](https://bgaapp.fly.dev/admin)

---

## 📅 Roadmap: Future Features

- Backfill complete **results history from 2019–2024**
- Public **player bios** with headshots, nicknames, and sortable stats
- Tournament **photo galleries**
- **Interactive charts and filters** for advanced stat breakdowns
- Team signup form for **upcoming events**
- Admin modals for easier score editing/deletion
- Smarter logic for **course-specific par values**

---

## 📸 Screenshots (Coming Soon)

Stay tuned! Visual walkthrough of leaderboard, admin panel, and player profiles.

---

## 🧑‍💻 Author

Built by [Alex Jungers](https://github.com/ajungers-ga) — Software Engineer, golfer, stats nerd
