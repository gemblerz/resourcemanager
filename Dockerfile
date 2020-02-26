FROM waggle/plugin-base-light:0.1.0

WORKDIR /app

COPY requirements.txt .
RUN pip3 --no-cache-dir install -r requirements.txt

COPY src/* /app/
ENTRYPOINT ["python3", "resourcemanager.py"]
