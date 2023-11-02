FROM python:3.6.12-alpine3.12

ENV OUTPUT_PATH=/home/rundeck/server/data/inventory/vcenter
ENV VCENTER_HOSTNAME=vcenter.example.com
ENV VCENTER_USERNAME=administrator@vsphere.local
ENV VCENTER_PASSWORD=password
ENV LINUX_USER=rundeck
ENV LINUX_EXECUTOR=jsch-ssh
ENV LINUX_COPIER=jsch-ssh
ENV LINUX_SETTINGS={}
ENV WINDOWS_USER=rundeck
ENV WINDOWS_EXECUTOR=WinRMPython
ENV WINDOWS_COPIER=WinRMPython
ENV WINDOWS_SETTINGS={}
ENV OTHER_USER=rundeck
ENV OTHER_EXECUTOR=jsch-ssh
ENV OTHER_COPIER=jsch-ssh
ENV OTHER_SETTINGS={}

RUN mkdir -p /app
WORKDIR /app

COPY . /app
RUN pip3 install -r requirements.txt
RUN crontab crontab
RUN mkdir -p /home/rundeck/server/data
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT /app/entrypoint.sh