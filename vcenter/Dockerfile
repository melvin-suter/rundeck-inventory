FROM python:3.6.12-alpine3.12

ENV OUTPUT_PATH=/export/inventory/vcenter
ENV VCENTER_HOSTNAME=vcenter.example.com
ENV VCENTER_USERNAME=administrator@vsphere.local
ENV VCENTER_PASSWORD=password

COPY . .
RUN pip install -r requirements.txt
RUN crontab crontab

CMD ["crond", "-f"]