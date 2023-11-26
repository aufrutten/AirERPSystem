FROM node:lts-slim

LABEL maintainer="aufrutten@gmail.com"

WORKDIR /app/
COPY package*.json ./
RUN npm install --silent
COPY . .

EXPOSE 80

RUN chmod -R +x /app/scripts/
CMD ["/app/scripts/entrypoint.sh"]
