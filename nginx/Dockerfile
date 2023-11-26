FROM nginx

LABEL maintainer="aufrutten@gmail.com"

# Setting the path to certs, keys and configs
ENV CERT_SSL="/etc/nginx/ssl/cert.pem"
ENV CERT_KEY="/etc/nginx/ssl/key.pem"
ENV OPENSSL_CONFIG="/etc/nginx/ssl/openssl.cnf"

# Remove default files and configurations
RUN rm /etc/nginx/conf.d/default.conf

# Copying the configs
COPY ./prod/ /etc/nginx/templates/
COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./ssl/openssl.cnf ${OPENSSL_CONFIG}

COPY ./scripts /scripts/
RUN chmod -R +x /scripts/

# Installing the certs utilitys
RUN apt install -y openssl

# Getting cert and key for developing
RUN openssl req -config ${OPENSSL_CONFIG} -nodes -x509 -newkey rsa:4096 -keyout ${CERT_KEY} -out ${CERT_SSL} -days 3650

# Opening ports
EXPOSE 80 443

# Running tests
RUN nginx -t || exit 1

CMD ["/bin/sh", "-c", "/scripts/entrypoint.sh"]
