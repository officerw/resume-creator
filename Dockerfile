# install base python image
FROM python:3.12

# Create app working directory
WORKDIR /app

# Install dependencies
COPY ./backend/requirements.txt .
RUN pip install -r requirements.txt

# Copy source code and latex templates
COPY ./backend/app.py .
COPY ./backend/createpdf.py .
COPY ./backend/tex_templates/* .

# Run the application
CMD ["python", "app.py"]