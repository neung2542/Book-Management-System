# Book-Management-System
book management system - FastAPI, nuxt, mySQL

---

## API Endpoints

- `GET    /books/`           — List books (supports `offset` and `limit`)
- `POST   /books/`           — Create a new book
- `GET    /books/{id}`       — Get a book by ID
- `PATCH  /books/{id}`       — Update a book
- `DELETE /books/{id}`       — Delete a book

---

## Features

- [ ] Authentication (JWT)
- [x] Responsive Design
- [x] Pagination
- [x] Loading / Error State
- [ ] Logging และ Error Handling
- [ ] Unit Test **
- [x] Document API **

---


## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/book-management-system.git
cd book-management-system
```

---

### 2. Backend Setup (FastAPI)

#### Install dependencies

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
```

#### Run the backend server

```bash
fastapi dev main.py
```

### 3. Frontend Setup (Nuxt 3)

#### Install dependencies

```bash
cd frontend
npm install
```

#### Run the frontend dev server

```bash
npm run dev
```

- The app will be available at `http://localhost:3000`
- API docs: `http://127.0.0.1:8000/docs`
