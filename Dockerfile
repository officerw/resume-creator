# install base python image
FROM python:3.12

# Create app directory
WORKDIR /app

# Install dependencies
COPY ./backend/requirements.txt /app
RUN pip install -r requirements.txt


# Copy source code and latex templates
COPY ./backend/app.py /app
COPY ./backend/createpdf.py /app
COPY ./backend/tex_templates/* /app