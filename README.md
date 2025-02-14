# 11-Minute Medicine Delivery API

## Overview
This project is designed to support the backend system for an 11-minute medicine delivery platform. The system includes endpoints for managing entities such as users, orders, and stores. It provides a RESTful API with a Swagger UI interface for easy testing and exploration of endpoints.

---

## Features
- PostgreSQL database setup and integration.
- RESTful API endpoints for CRUD operations.
- Swagger UI for API documentation and testing.
- Asynchronous server using Uvicorn.

---

## Prerequisites
Ensure the following software is installed on your system:
- Python 3.9+
- PostgreSQL
- Git

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Set Up PostgreSQL Database
1. Install PostgreSQL if it is not already installed.
2. Start the PostgreSQL service.
3. Use the following credentials to set up the database:
   - Database: `postgres`
4. Update the database connection URI in `database.py`:
   ```python
   DATABASE_URI = "postgresql://<username>:<password>@localhost:5432/postgres"
   ```
   Replace `<username>` and `<password>` with your PostgreSQL credentials.

### 3. Create Tables
Run the following command to initialize the database tables:
```bash
python init_db.py
```

### 4. Start the Application
Run the application using Uvicorn:
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8081
```

---

## Accessing the API
1. Open your web browser.
2. Navigate to the Swagger UI:
   ```
   http://localhost:8081/docs
   ```
3. Test the available endpoints.
   > **Note:** Exclude any endpoints related to the `entity` module for now.

---

## Folder Structure
```
.
├── app.py            # Main application file
├── database.py       # Database configuration file
├── init_db.py        # Script to initialize the database tables
├── models/           # Contains database models for entities
├── controllers/      # API route handlers
├── dal/              # Data Access Layer
├── requirements.txt  # Python dependencies
└── README.md         # Project documentation
```

---

## Dependencies
Install the required dependencies using:
```bash
pip install -r requirements.txt
```

---

## Notes
- Ensure PostgreSQL is running before starting the application.
- Update the database connection URI in `database.py` as needed.

---

## Troubleshooting
### Common Issues
1. **Database Connection Error:**
   - Ensure PostgreSQL service is running.
   - Verify the credentials and database URI in `database.py`.

2. **Module Not Found Errors:**
   - Check that all dependencies are installed via `requirements.txt`.

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

