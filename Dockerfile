FROM ubuntu:latest

RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
RUN apt-get upgrade -y
RUN apt-get install -y texlive
RUN apt-get install -y python3
RUN apt install -y pipx

# Create app working directory
WORKDIR /app

# Install dependencies
COPY ./backend/requirements.txt .
RUN pipx install Flask
RUN pipx install Flask_Cors
RUN pipx install pdflatex

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