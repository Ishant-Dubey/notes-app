# Notes App

A small notes application with a FastAPI backend, a Streamlit frontend, SQLAlchemy for database persistence, and Supabase authentication.

## Features

* Sign up and log in with email and password
* Create, view, edit, and delete personal notes
* Protect note operations with Supabase bearer tokens
* Store notes using SQLAlchemy
* Associate each note with the authenticated Supabase user
* Restrict users to their own notes

## Requirements

* Python 3.13 or newer
* PostgreSQL database
* A Supabase project with email/password authentication enabled
* [uv](https://docs.astral.sh/uv/)

## Configuration

### Backend

Create a `.env` file in the project root:

```env
DATABASE_URL=your-database-connection-string
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key
```

Do not commit `.env` or expose these values publicly.

### Frontend

The Streamlit frontend reads the backend address from Streamlit secrets.

Create:

```text
.streamlit/secrets.toml
```

in the project root:

```toml
BACKEND_URL = "http://127.0.0.1:8000"
```

For deployment, set `BACKEND_URL` to the deployed backend URL instead of the local address.

Keep `BACKEND_URL` as the backend base URL. The frontend appends routes such as `/login`, `/signup`, and `/notes`.

## Installation

From the project root:

```bash
uv sync
```

## Running the Application

### Start the backend

From the project root:

```bash
cd backend
uv run uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### Start the frontend

Open a second terminal from the project root:

```bash
streamlit run frontend/Login.py
```

The Streamlit frontend reads the backend address from `.streamlit/secrets.toml`.

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
Notes/
├── backend/
│   ├── database.py       SQLAlchemy engine and database sessions
│   ├── main.py           FastAPI application and routes
│   ├── models.py         Database models
│   └── schemas.py        Pydantic request and response schemas
│
├── frontend/
│   ├── Login.py          Streamlit login page
│   └── pages/
│       ├── 1_Sign_Up.py  Sign-up page
│       └── 2_Notes.py    Notes page
│
├── .streamlit/
│   └── secrets.toml      Local Streamlit secrets
│
├── pyproject.toml
├── uv.lock
└── .gitignore
```

## Deployment

The backend and frontend are deployed separately.

### Backend

The FastAPI backend is deployed as a web service. Configure the following environment variables on the backend hosting platform:

```text
DATABASE_URL
SUPABASE_URL
SUPABASE_KEY
```

The backend is started with:

```bash
cd backend && uv run uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Frontend

The Streamlit frontend is deployed separately.

Configure the following Streamlit secret:

```toml
BACKEND_URL = "https://your-deployed-backend-url"
```

The frontend uses this value to communicate with the deployed FastAPI backend.

## Notes

* The backend creates the `notes` table when it starts.
* Each note is associated with the authenticated Supabase user's ID.
* Protected note operations require a valid Supabase bearer token.
* Users can only access and modify their own notes.
* The frontend gets the backend address from `BACKEND_URL`.
* `.env` and `.streamlit/secrets.toml` should not be committed to Git.
