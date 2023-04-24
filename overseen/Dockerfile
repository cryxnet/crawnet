# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

# Set the working directory to /app
WORKDIR /overseen

# Copy the current directory contents into the container at /app
COPY . /overseen

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

WORKDIR /overseen/app

# Run app.py when the container launches
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
