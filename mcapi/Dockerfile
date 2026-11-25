# FROM nginx:latest
FROM python:3.10

# set working directory
WORKDIR /api/mcapi

# copy requirements
COPY requirements.txt tmp/requirements.txt

# install required packages 
RUN pip install --no-cache-dir -r tmp/requirements.txt \
        && pip install --no-cache-dir "fastapi[standard]"

# copy application files
COPY Dockerfile main.py models.py search.py ./

# start FastAPI
CMD ["fastapi", "dev", "main.py", "--host", "0.0.0.0", "--port", "8000"]