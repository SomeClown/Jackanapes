FROM alpine:3.5

ENV ALPINE_VERSION=3.5

ENV PACKAGES="\
	dumb-init \
	bash \
	python3 \
"


RUN apk update \
	&& apk upgrade \
	&& apk add python3 \
	&& apk add python3-dev \
	&& apk add bash \
	&& pip3 install --upgrade pip \
	&& apk add git
	

WORKDIR /jackanapes/app
ADD . /jackanapes

RUN pip3 install -r /jackanapes/app/requirements.txt
