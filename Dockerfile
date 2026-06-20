# ---- Stage 1: build -----------------------------------------------------------
# Install dependencies into a clean prefix we can copy into the final image.
FROM python:3.12-slim AS build

WORKDIR /install

COPY requirements.txt .
# Install deps into /install/deps so we can copy just that layer later.
RUN pip install --no-cache-dir --prefix=/install/deps -r requirements.txt


# ---- Stage 2: runtime ---------------------------------------------------------
# Final image is small and runs as a non-root user.
FROM python:3.12-slim AS runtime

# Create a non-root user (case explicitly asks for non-root).
RUN useradd --create-home --uid 10001 appuser

WORKDIR /home/appuser/app

# Copy installed dependencies from the build stage.
COPY --from=build /install/deps /usr/local

# Copy the application code.
COPY app/ ./app/

# Drop privileges.
USER appuser

ENV PORT=8080
EXPOSE 8080

# gunicorn is a production-grade WSGI server (better than flask's dev server).
# 2 workers is plenty for this tiny service.
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "app.main:app"]
