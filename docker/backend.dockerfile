FROM python:3.8

# Set env variables
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install dependencies for opencv package
RUN apt update && \
    apt -y install libgl1-mesa-glx

RUN pip install setuptools aiohttp

RUN git clone https://github.com/tus/tus-py-client.git
RUN cd tus-py-client && \
    python setup.py install

# Copy pipenv files
COPY Pipfile* ./

# Install dependencies
RUN pip install pipenv && pipenv install --system

# Copy code
COPY /src ./src

# Set PYTHONPATH
ENV PYTHONPATH "/app/src:${PYTHONPATH}"

CMD ["python", "src/main.py"]
