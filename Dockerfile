FROM --platform=linux/amd64 alpine:3.14

RUN apk update && \
    apk add --no-cache python3 python3-dev py3-pip nginx && \
    apk add --no-cache gcc musl-dev && \
    rm -rf /var/cache/apk/*

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

COPY . /app

# Remove default.conf if it exists
#RUN rm -f /etc/nginx/conf.d/default.conf || true

# Copy your custom nginx.conf to the conf.d directory
#COPY nginx.conf /etc/nginx/conf.d/

EXPOSE 8000
ENTRYPOINT [ "python3" ]
CMD ["app.py"]
