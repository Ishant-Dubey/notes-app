# Notes App

A small notes application with a FastAPI backend, a Streamlit frontend, SQLAlchemy persistence, and Supabase authentication.

## Features

* Sign up and log in with email and password
* Create, view, edit, and delete personal notes
* Protect note operations with Supabase bearer tokens
* Store notes using SQLAlchemy
* Associate each note with the authenticated Supabase user

## Requirements

* Python 3.13 or newer
* A database supported by SQLAlchemy
* A Supabase project with email/password authentication enabled
* `uv` or another Python package manager

## Configuration

Create a `.env` file in the project root:

```env
DATABASE_URL=your-database-connection-string

SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key
```

Do not commit `.env` or expose these values publicly.

## Installation

From the project root, install the dependencies:

```bash
uv sync
```

Alternatively, install the project and its dependencies with pip:

```bash
pip install -e .
```

## Running the Application

### Start the backend

From the `backend` directory:

```bash
cd backend
uv run uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### Start the frontend

In a second terminal, from the project root:

```bash
streamlit run frontend/Login.py
```

The Streamlit frontend expects the API to be available at:

```text
http://127.0.0.1:8000
```

### API Documentation

Once the backend is running:

* Swagger UI: `http://127.0.0.1:8000/docs`
* ReDoc: `http://127.0.0.1:8000/redoc`

## API Endpoints

| Method   | Endpoint           | Authentication | Description                       |
| -------- | ------------------ | -------------- | --------------------------------- |
| `GET`    | `/`                | No             | Health and welcome response       |
| `POST`   | `/signup`          | No             | Create a Supabase user            |
| `POST`   | `/login`           | No             | Log in and return an access token |
| `POST`   | `/notes`           | Bearer token   | Create a note                     |
| `GET`    | `/notes`           | Bearer token   | List the current user's notes     |
| `PUT`    | `/notes/{note_id}` | Bearer token   | Update a note                     |
| `DELETE` | `/notes/{note_id}` | Bearer token   | Delete a note                     |

## Request Examples

### Sign Up or Log In

```json
{
  "email": "johndoe@example.com",
  "password": "your-password"
}
```

### Create or Update a Note

```json
{
  "title": "Shopping list",
  "content": "Milk, bread, and fruit"
}
```

### Authentication

For protected endpoints, send the access token returned after a successful login:

```text
Authorization: Bearer <access-token>
```

Depending on your Supabase authentication settings, a signup response may also include a session and access token.

## Project Structure

```text
backend/
    database.py         SQLAlchemy engine and database sessions
    main.py             FastAPI application and routes
    models.py           Database models
    schemas.py          Pydantic request and response schemas

frontend/
    Login.py            Streamlit login page
    pages/
        1_Sign_Up.py    Sign-up page
        2_Notes.py      Notes page
```

## Notes

* The backend creates the `notes` table when it starts.
* Each note is associated with the authenticated Supabase user's ID.
* Note operations are protected using Supabase bearer tokens.
* Users can only access and modify their own notes.
* The Streamlit pages currently use the local API URL `http://127.0.0.1:8000`.
* For deployment, the frontend API URL must be changed to the deployed backend URL.
