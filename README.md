# 🏨 The Grand Jakarta Hotel

A full-stack luxury hotel booking web application built with **Vue.js 3** (Frontend) and **FastAPI** (Backend). This project features a modern UI, JWT authentication, QRIS/Virtual Account dummy payment, and a looping video background on the hero section.

![Vue.js](https://img.shields.io/badge/Vue.js-3.x-4FC08D?logo=vue.js)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?logo=fastapi)
![SQLite](https://img.shields.io/badge/SQLite-3-blue?logo=sqlite)

---

## 📸 Preview

- **Hero Section**: Looping video background.
- **Rooms**: Display available suites with prices and features.
- **Booking**: Choose QRIS or Virtual Account (Dummy payment).
- **Authentication**: Register & Login with JWT token.
- **My Bookings**: View all confirmed reservations.

---

## 🚀 Tech Stack

### Backend
- **Framework**: FastAPI
- **Database**: SQLite (SQLAlchemy ORM)
- **Authentication**: JWT (python-jose) + bcrypt
- **Validation**: Pydantic
- **Server**: Uvicorn

### Frontend
- **Framework**: Vue 3 (Composition API)
- **State Management**: Pinia
- **Routing**: Vue Router
- **HTTP Client**: Axios
- **Build Tool**: Vite

---

## 📋 Prerequisites

Make sure you have the following installed on your machine:

- **Python** 3.12 or higher (3.14 is supported if SQLAlchemy >= 2.0.31)
- **Node.js** 18 or higher
- **npm** or **yarn**
- **Git**

---

## 🔧 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/RaihanAhsan/hotel-app.git
cd hotel-app
