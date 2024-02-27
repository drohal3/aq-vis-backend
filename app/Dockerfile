FROM python:3.11
WORKDIR /app
COPY . /app
# CMake is needed to build and install awscrt from source
#RUN apt-get update && apt-get -y install cmake

RUN pip install -r ./requirements.txt

EXPOSE 8000

# No need for multi-stage build in python
CMD ["uvicorn", "src.main:app", "--reload", "--host=backend"]