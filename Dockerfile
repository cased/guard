FROM python:3

WORKDIR /usr/src/app

COPY . ./
RUN ./local-install

ENV TERRAFORM_VERSION 0.12.7
ENV PATH="/root/.cguard/shims:${PATH}"

RUN mkdir -p /root/.cguard/shims

RUN cd /usr/local/bin && \
    curl https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip -o terraform_${TERRAFORM_VERSION}_linux_amd64.zip && \
    unzip terraform_${TERRAFORM_VERSION}_linux_amd64.zip && \
    rm terraform_${TERRAFORM_VERSION}_linux_amd64.zip

RUN cased url http://host.docker.internal:3000/api

CMD ["/bin/bash"]