FROM alpine:edge

ADD . /

RUN apk add --update build-base python3-dev && \
	cp manifest.json /var/manifest.json && \
	pip3 install virtualenv && \
	pip3 install -r requirements.txt

ENTRYPOINT ["make", "run"]
