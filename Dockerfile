FROM python:3.12

# Install ImageMagick
RUN apt-get update && \
    apt-get install -y imagemagick

# Install Python packages
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the Streamlit app
COPY app.py /app/app.py

# Set the working directory
WORKDIR /app

# Command to run the app
CMD ["streamlit", "run", "app.py"]
