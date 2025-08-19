FROM public.ecr.aws/lambda/python:3.13-x86_64

WORKDIR /var/task

COPY requirements.txt .
RUN pip install -r requirements.txt -t .

COPY lambda_function.py .
