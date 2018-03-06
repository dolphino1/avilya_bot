FROM python:3.6.1

# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# add requirements (to leverage Docker cache)
ADD ./requirements.txt /usr/src/app/requirements.txt

# install requirements
RUN pip --default-timeout=1000 install -r requirements.txt

#Download spacy tolkenizer
RUN python -m spacy download en_core_web_lg

# add app
ADD . /usr/src/app

# run server
CMD python rasa_api/run_server.py runserver -h 0.0.0.0
