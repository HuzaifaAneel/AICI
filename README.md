# Full Stack Application Setup

This project consists of a **backend** (FastAPI) and a **frontend** (React). Below are instructions to run the backend, frontend, and the entire app using Docker and Docker Compose.

---

## Backend Setup

### Environment Variables

The backend requires the following environment variables:

- `MONGO_URI`: The MongoDB connection URI (e.g., `mongodb://localhost:27017` for local MongoDB).
- `SECRET_KEY`: The secret key used for JWT authentication.
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time in minutes. (e.g. 30)

### Running the Backend

To run the backend:

1. Navigate to the backend directory:

    ```bash
    cd backend
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Export the required environment variables and run the backend:

    #### For Bash:
    ```bash
    export MONGO_URI="mongodb://localhost:27017"
    export SECRET_KEY="your-secret-key"
    export ACCESS_TOKEN_EXPIRE_MINUTES="30"
    uvicorn main:app --host 0.0.0.0 --port 8080 --reload
    ```

    #### For PowerShell:
    ```powershell
    $env:MONGO_URI="mongodb://localhost:27017"
    $env:SECRET_KEY="your-secret-key"
    $env:ACCESS_TOKEN_EXPIRE_MINUTES="30"
    uvicorn main:app --host 0.0.0.0 --port 8080 --reload
    ```

4. The backend will be running on `http://localhost:8080`.

---

## Frontend Setup

### Running the Frontend

1. Navigate to the frontend directory:

    ```bash
    cd frontend
    ```

2. Install dependencies:

    ```bash
    npm install
    ```

3. Run the frontend in development mode:

    ```bash
    npm start
    ```

4. The frontend will be available at `http://localhost:3000`.

---

## Running the App with Docker Compose

### Prerequisites

- [Docker](https://www.docker.com/get-started) installed on your machine.
- [Docker Compose](https://docs.docker.com/compose/install/) installed.

### Steps


1. Run the following command to build and run both the backend and frontend:

    #### For PowerShell:
    ```powershell
    $env:MONGO_URI="URL"; $env:SECRET_KEY="Secret_Key"; $env:ACCESS_TOKEN_EXPIRE_MINUTES="30"; docker-compose up --build
    ```

2. Docker will:
    - Build and start the backend service on port `8080`.
    - Build and serve the frontend on port `3000`.

3. Access the services:
    - **Frontend**: [http://localhost:3000](http://localhost:3000)
    - **Backend**: [http://localhost:8080](http://localhost:8080)

### Stopping the Services

To stop the services, run:

```bash
docker-compose down
