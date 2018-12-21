FROM python:3.6
MAINTAINER @rafeatw

ENV FLASK_PATH /usr/src/flaskreco

# set working dir
COPY . /$FLASK_PATH
WORKDIR $FLASK_PATH

# upgrade pip
RUN pip install --upgrade pip

# install Python modules needed by the Python app
RUN pip install --no-cache-dir -r $FLASK_PATH/requirements.txt

# tell the port number the container should expose
EXPOSE 5000

# run the application
# CMD ["python", "/usr/src/flaskreco/wsgi.py"]
# /usr/local/bin/gunicorn --workers 3 --bind unix:fldoaskreco.sock -m 007 wsgi:app
# CMD ["/usr/local/bin/gunicorn", "--config", "/usr/src/flaskreco/gunicorn.conf", "wsgi:app"]


# docker build -t rafeatw/flaskreco .
# docker run -p 8888:5000 --name flaskreco --rm rafeatw/flaskreco
# http://localhost:8888/