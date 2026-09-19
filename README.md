# Campus Flora Information Management System (PlantBase - PUPQC)

**PlantBase** is a Campus Flora Information Management System designed for **PUP Quezon City** to help students, faculty, staff, and visitors explore, research, and learn about the different plants found across the campus. It provides organized plant information through a modern, responsive, and user-friendly platform.

Built with **Python Flask**, **MySQL**, **HTML5**, **CSS3**, **JavaScript**, and **Bootstrap 5**.

---

## 🛠️ Tech Stack & Architecture

- **Frontend**: HTML5, CSS3, JavaScript (ES6+), Bootstrap 5 framework.
- **Backend**: Python 3 (Flask Framework, REST API endpoints).
- **Database**: 
  - **Primary**: MySQL (`pupqc_plant_db` schema provided in `schema.sql`).
  - **Auto-Fallback**: Integrated SQLite fallback (`pupqc_plant_db.sqlite`) pre-seeded with sample flora data so the application runs instantly even before configuring MySQL credentials.
- **Styling**: PUP Maroon (`#800000`) & Gold (`#FFC107`) university visual identity.

---

## 📂 Project Directory Structure

```text
RESEARCH/
├── app.py                      # Main Flask Web Application Server & REST API
├── db_config.py                # Database connection manager (MySQL & SQLite fallback)
├── schema.sql                  # MySQL database creation & seed data script
├── requirements.txt            # Python dependencies
├── create_placeholders.py      # Helper script for SVG header graphic
├── templates/
│   ├── index.html              # Main User Website (Maroon theme, Hero, Filterable Grid, Modals)
│   └── admin.html              # Admin Management Dashboard (CRUD Operations)
├── static/
│   ├── css/
│   │   └── style.css           # Custom PUPQC theme CSS stylesheet
│   ├── js/
│   │   └── main.js             # Dynamic search, category filtering, and modal API calls
│   └── images/
│       ├── campus_header.jpg              # PUPQC Campus Entrance Header Photo
│       └── campus_header_placeholder.svg  # Default Header Photo Placeholder
└── README.md                   # Complete documentation
```

---

## 🚀 Quick Start Guide

### 1. Install Required Python Packages
Open your terminal in the project directory and run:
```bash
pip install -r requirements.txt
```

### 2. (Optional) Setup MySQL Database
To use your local MySQL server (XAMPP / MySQL Workbench):
1. Import `schema.sql` into MySQL:
   ```bash
   mysql -u root -p < schema.sql
   ```
2. (Optional) Set environment variables if your MySQL credentials differ from defaults (`localhost`, `user: root`, `password: ""`):
   - `MYSQL_HOST` (default: `localhost`)
   - `MYSQL_USER` (default: `root`)
   - `MYSQL_PASSWORD` (default: `""`)
   - `MYSQL_DB` (default: `pupqc_plant_db`)

> **Note**: If MySQL is not running, the application automatically runs using the embedded SQLite database so you can test and demonstrate the app right away!

### 3. Launch Flask Server
Run the application server:
```bash
python app.py
```
Open your web browser and navigate to:
```text
http://127.0.0.1:5000
```

---

## 🌟 Key Features

- **PUP Maroon & Gold Theme**: Customized based on PUPQC school design specifications.
- **Real-Time Search & Category Filters**: Search campus flora by common name, scientific name, plant family, or campus location.
- **Detailed Flora Modals**: Inspect conservation status, botanical descriptions, traditional/medicinal uses, and campus locations.
- **Admin Management Portal**: Add, edit, or delete plant records directly (`/admin`).
- **Cookie Notice Bar**: UI element matching reference design screenshot.
