# Face-It

This API allows you to compare two face images to determine if they match and provides the Euclidean distance between the face encodings.

## Requirements

- Python 3.11+
- virtualenv

## Setup

1. **Clone the repository:**

    ```sh
    git clone <repository_url>
    cd face-it
    ```

2. **Create a virtual environment:**

    ```sh
    python -m venv venv
    ```

3. **Activate the virtual environment:**

    - On Windows:

        ```sh
        venv\Scripts\activate
        ```

    - On macOS/Linux:

        ```sh
        source venv/bin/activate
        ```

4. **Install dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

## Running the API

1. **Start the Flask application:**

    ```sh
    python app.py
    ```

2. The API will be available at `http://127.0.0.1:5000`.

## Making Requests

Use `curl` or any HTTP client to make a POST request to the `/compare` endpoint.

### Example using `curl`:

```sh
curl -X POST http://127.0.0.1:5000/compare \
    -F "known_image=@/path/to/known_image.jpeg" \
    -F "compared_image=@/path/to/compared_image.jpeg"
```

### Response 

```sh
  {
    "match": true,
    "distance": 0.45
  }
```

## Run with Docker Container

1. Create a dockerfile at the root of your project.

```
# Use the official Python image from the Docker Hub
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0"]
 
```

2. Build Docker Image

```
  docker build -t face-recognition-api .

```

3. Run the Docker container 

```
  docker run -p 5000:5000 face-recognition-api

```

- The API should now be accessible at http://localhost:5000.

# Notes

- Ensure that the image files provided in the requests are in a valid format supported by the Pillow library.
- This API is intended for development and testing purposes. For production deployment, consider using a production WSGI server like Gunicorn.
- The Docker setup provided here is for basic usage. Adjust the Dockerfile and related configurations as needed for your specific deployment requirements.