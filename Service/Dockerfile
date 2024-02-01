FROM python:3.10.4

WORKDIR /app
COPY . .
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
CMD python /app/main.py