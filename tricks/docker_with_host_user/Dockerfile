FROM python:3.6-alpine

# the default won't work everywhere, but it should be OK where I want to use it
ARG USER_ID=1000
ARG GROUP_ID=1000

# if the IDs are not set, just create some user
RUN addgroup -S -g $GROUP_ID django
RUN adduser -G django -S -s /bin/sh -u $USER_ID django

RUN mkdir /app
RUN chown django:django /app

USER django
WORKDIR /app

CMD ["sh"]
