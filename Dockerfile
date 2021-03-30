FROM python:3.9

WORKDIR /usr/src/app

COPY . ./
RUN ./dev-install

ENV TERRAFORM_VERSION 0.12.7
ENV PATH="/root/.cguard/shims:${PATH}"
ENV CASED_RECORDING_ENABLED 1


RUN mkdir -p /root/.cguard/shims

RUN cd /usr/local/bin && \
    curl https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip -o terraform_${TERRAFORM_VERSION}_linux_amd64.zip && \
    unzip terraform_${TERRAFORM_VERSION}_linux_amd64.zip && \
    rm terraform_${TERRAFORM_VERSION}_linux_amd64.zip

RUN \
  apt-get update && \
  apt-get install -y ruby && \
  apt-get install -y ruby-dev && \
  gem install rails

RUN cased url http://host.docker.internal:3000/api

CMD ["/bin/bash"]
