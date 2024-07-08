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
COPY ./backend/tex_templates/template1.tex .
COPY ./backend/tex_templates/template2.tex .
COPY ./backend/tex_templates/template3.tex .
COPY ./backend/tex_templates/template4.tex .
COPY ./backend/tex_templates/template5.tex .

# Run the application
CMD ["python", "app.py"]