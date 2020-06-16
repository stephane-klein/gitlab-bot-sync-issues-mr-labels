FROM python:3.6-alpine
ENV PYTHONUNBUFFERED=true

WORKDIR /src/
ADD ./requirements.txt /src/

RUN apk update && apk upgrade
RUN apk add --no-cache gcc python3-dev musl-dev \
  && pip install --upgrade pip \
  && pip install -r requirements.txt \
  && apk del gcc python3-dev musl-dev

ADD ./main.py /src/main.py
ADD ./utils.py /src/utils.py

ENV GL_SECRET=secret
ENV GL_ACCESS_TOKEN=secret
ENV GL_URL=https://gitlab.com

CMD python main.py