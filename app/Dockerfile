FROM python:3.11
WORKDIR /app
COPY . .
# CMake is needed to build and install awscrt from source
#RUN apt-get update && apt-get -y install cmake
# Expose port 8000, which is the default port for Uvicorn
EXPOSE 8000

RUN pip install -r ./requirements.txt
CMD ["uvicorn", "main:app", "--reload", "--host=backend"]