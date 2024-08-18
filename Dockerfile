FROM python:3.12
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /worstshop
COPY requirements.txt /worstshop/
RUN pip install -r requirements.txt
COPY . /worstshop/
