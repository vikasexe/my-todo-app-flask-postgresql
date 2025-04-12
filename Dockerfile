# Base image
FROM python:3.9

# create work directory
WORKDIR /usr/src/app

# copy app files to image
COPY . .

# upgrade pip version 
RUN pip install --upgrade pip

# install the dependencies in requirements.txt without using the cache
RUN pip install --no-cache-dir -r requirements.txt

# container listens on port 5000.
EXPOSE 5000


# Run the application.
CMD ["python", "./app.py"]