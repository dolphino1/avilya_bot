FROM python:3.6.1

# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# add requirements (to leverage Docker cache)
ADD ./requirements.txt /usr/src/app/requirements.txt

# install requirements
RUN pip --default-timeout=1000 install -r requirements.txt

# add app
ADD . /usr/src/app

# run slack client
CMD python -u slack_bot/run.py

