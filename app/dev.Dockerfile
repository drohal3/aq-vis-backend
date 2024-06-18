FROM python:3.11 as test
WORKDIR /app
COPY . /app
# CMake is needed to build and install awscrt from source
# RUN apt-get update && apt-get -y install cmake

RUN pip install -r ./requirements.txt
RUN pip install -r ./requirements_dev.txt

CMD ["uvicorn", "src.main:app", "--reload", "--host=backend"]