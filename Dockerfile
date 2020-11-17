FROM python:3

# copy project
COPY . /

# set timezone so that tzdata doesn't prompt interactively
ENV TZ=America/Chicago
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# install libs
RUN apt-get update
RUN apt-get -y install git libxslt-dev libxml2-dev python3-lxml python3-crypto

# install requirements 
RUN pip3 install -r requirements.txt

# copy settings file
RUN cp tapiriik/local_settings.py.example tapiriik/local_settings.py

# generate keys
RUN python3 credentialstore_keygen.py >> tapiriik/local_settings.py

# run server, worker and scheduler
ENTRYPOINT python3 manage.py runserver 0.0.0.0:8000 && python3 sync_worker.py && python3 sync_scheduler.py