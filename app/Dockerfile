FROM python:3.11-slim
WORKDIR /app
COPY . /app
# CMake is needed to build and install awscrt from source
#RUN apt-get update && apt-get -y install cmake

RUN pip install -r ./requirements.txt &&\
    adduser --system --group appuser &&\
    chown appuser .

USER appuser

EXPOSE 8000

# No need for multi-stage build in python
# TODO: host should be backend?
CMD ["uvicorn", "src.main:app", "--reload", "--host=0.0.0.0"]