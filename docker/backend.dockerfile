FROM python:3.8

# Set env variables
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Copy pipenv files
COPY Pipfile* ./

# Install dependencies for opencv package
RUN apt update && apt -y install libgl1-mesa-glx

# Install dependencies
RUN pip install pipenv && pipenv install --system

# Copy code
COPY /src ./src

# Set PYTHONPATH
ENV PYTHONPATH "/app/src:${PYTHONPATH}"

CMD ["python", "src/main.py"]
