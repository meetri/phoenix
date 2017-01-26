FROM centos:7
LABEL maintainer "Demetrius Bell <meetri@gmail.com>"

RUN yum install -y gcc epel-release \
&& yum install -y python-pip python-devel \
&& pip install --upgrade pip \
&& pip install flask pyephem pytz egenix-mx-base argparse tzlocal

COPY app /opt/phoenix/app/
COPY phoenix /opt/phoenix/phoenix/

WORKDIR /opt/phoenix/app

ENTRYPOINT ["/opt/phoenix/app/run"]
