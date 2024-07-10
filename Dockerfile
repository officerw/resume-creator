# Install base texlive image
FROM texlive/texlive:latest

# Install pip
RUN apt-get -y install python3-pip

# Create app working directory
WORKDIR /app

# Install dependencies
COPY ./backend/requirements.txt .
RUN pip install -r requirements.txt

# Copy source code and latex templates
COPY ./backend/app.py .
COPY ./backend/createpdf.py .

WORKDIR /app/tex_templates

COPY ./backend/tex_templates/template1.tex .
COPY ./backend/tex_templates/template2.tex .
COPY ./backend/tex_templates/template3.tex .
COPY ./backend/tex_templates/template4.tex .
COPY ./backend/tex_templates/template5.tex .

WORKDIR /app

# Run the application
CMD ["python", "app.py"]