FROM python:3-alpine

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN pip install --no-cache-dir .

ENTRYPOINT ["cfn-flip"]
