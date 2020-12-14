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
RUN cp tapiriik/local_settings.py.os tapiriik/local_settings.py

# generate static files
RUN python3 manage.py collectstatic --noinput

# run server, worker and scheduler
# override this when running online to provide only one of these commands
CMD python3 manage.py runserver 0.0.0.0:8000 --insecure && python3 sync_worker.py && python3 sync_scheduler.py
