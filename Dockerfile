FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    qemu-system-x86 \
    qemu-utils \
    proot \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN pip install -e .

ENTRYPOINT ["clinux"]