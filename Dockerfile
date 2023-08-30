FROM python:3.9
ARG BRANCH=main
RUN apt install git

RUN git clone --branch=$BRANCH https://github.com/WEBIGEO-ALTEN/WEBIGEO_BACK.git
RUN cd WEBIGEO_BACK
WORKDIR WEBIGEO_BACK/
RUN git pull
RUN pip install --no-cache-dir -r requierements.txt
EXPOSE 8000
CMD ["python3", "manage.py","runserver", "0.0.0.0:8000"]


