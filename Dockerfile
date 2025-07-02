# --------- Stage 1: Build Frontend ---------
FROM node:18-alpine AS frontend-build

WORKDIR /app

# Copy frontend source code
COPY ./frontend ./frontend

WORKDIR /app/frontend

# Install and build frontend
RUN npm install
RUN npm run build


# --------- Stage 2: Build Flask Backend ---------
FROM python:3.10-slim AS flask-backend

# Set workdir
WORKDIR /app

# Copy backend files
COPY ./backend ./backend

# Copy frontend build output to Flask static folder
COPY --from=frontend-build /app/frontend/dist /app/backend/static  # or build if using CRA

# Install dependencies
COPY ./backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask app port
EXPOSE 5000

# Set env vars
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the Flask app
WORKDIR /app/backend
CMD ["flask", "run"]
