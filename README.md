## About This Project

The purpose of this project is to learn and create a Flask web application that functions as a project management tool. The project involves setting up a local database, implementing simple authorization, and developing a frontend interface. This project is still in development and serves as a practical learning experience for the Flask development framework. Below is a detailed overview of the steps involved and the current stack used in this project.

#### Steps Involved:

1. **Setting Up a Local Database**:
    - The first step was setting up a local database using **SQLite**.

2. **Implementing Authorization**:
    - Simple authorization was set up using **Flask-JWT-Extended**. This extension provides JSON Web Token support for Flask.

3. **Testing Backend Routes**:
    - To ensure the backend routes were functioning correctly, **Postman** was used for testing the API endpoints. It allowed for testing of the routes before integrating and devloping the frontend.

4. **Creating a Simple Frontend**:
    - A basic frontend was developed using **HTML**, **CSS**, and **JavaScript**.

5. **Continuous Development**:
    - This project is an ongoing learning process, with continuous updates and improvements being made. The aim is to gain a deeper understanding of the Flask framework and to build a fully functional project management tool.

#### Current Stack:

- **Flask**
- **Flask-SQLAlchemy**
- **Flask-Migrate**
- **Flask-Bcrypt**
- **Flask-JWT-Extended**
- **Werkzeug**
- **SQLAlchemy**
- **Flask-Cors**
- **gunicorn**
- **gevent**
- **python-dotenv**


This project showcases the integration of various Flask extensions and tools to build a comprehensive web application. It serves as an educational journey to learn about the Flask framework and its ecosystem.

## Code Architecture

```
project_management_tool/
│
├── backend/
│   ├── __init__.py
│   ├── init.py
│   ├── auth.py
│   ├── models.py
│   ├── routes.py
│   ├── run.py
│   └── requirements.txt
│
├── frontend/
│   ├── app.js
│   ├── app.yaml
│   ├── index.html
│   ├── register.html
│   └── styles.css
│
├── utils/
│   └── generate_credentials.py
│
├── .gitignore
├── LICENSE
└── README.md
```
