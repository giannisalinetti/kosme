FROM registry.access.redhat.com/ubi9/python-311:latest

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY kosme.py .

USER 1001

ENTRYPOINT ["python", "kosme.py"]
