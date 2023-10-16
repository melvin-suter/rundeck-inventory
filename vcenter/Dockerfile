FROM python:3.6.12-alpine3.12

ENV OUTPUT_PATH=/home/rundeck/server/data/inventory/vcenter
ENV VCENTER_HOSTNAME=vcenter.example.com
ENV VCENTER_USERNAME=administrator@vsphere.local
ENV VCENTER_PASSWORD=password

RUN mkdir -p /app
WORKDIR /app

COPY . .
RUN pip3 install -r requirements.txt
RUN crontab crontab
RUN mkdir -p /home/rundeck/server/data
RUN chmod +x entrypoint.sh

ENTRYPOINT entrypoint.sh