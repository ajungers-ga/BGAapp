# 🏌️‍♂️ BGA League Tracker — Final Project (General Assembly)

This project is the **capstone of my Software Engineering program at General Assembly** — and a personal passion project I plan to maintain and grow for years to come.

It tracks events, players, and historical performance in the **Beast Golf Association**, a competitive and fun league touring the great Golf Courses in Minnesota.

---

## 🚀 Tech Stack

**Backend:**
- Python 3.11  
- Django 5.2  
- Django Admin  
- PostgreSQL (Fly.io Postgres cluster)

**Frontend:**
- Django Templates  
- Bootstrap 5  
- Custom CSS

**Deployment & DevOps:**
- Fly.io (Docker-based deployment)  
- Git & GitHub  
- Admin login & fixture data loading in production

---

## 🧠 New Tech I Learned On My Own

To bring this project to life, I stepped beyond the GA curriculum and learned:

- ✅ How to deploy a Django app using **Fly.io**
- ✅ How to provision and use a **PostgreSQL cluster in production**
- ✅ How to manage **CSRF protection** and domain trust settings in a live web app
- ✅ How to load clean fixture data in a Dockerized Django container
- ✅ Advanced Django modeling techniques including:
  - Calculated fields via `@property`
  - Finalized event logic
  - Tie/placement scoring with medals 🥇🥈🥉

---

## 🔒 Admin Panel (Live)

[https://bgaapp.fly.dev/admin](https://bgaapp.fly.dev/admin)

---

## 🌱 Future Features

- Full season-by-season results archive (backfilling 2019–2024)
- Public player profiles with headshots, nicknames, and stats
- Tournament photo galleries
- Interactive charts and filters
- Team builder + signup forms for upcoming events
