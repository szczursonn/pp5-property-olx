FROM node:18-alpine

WORKDIR /app

COPY . .

RUN npm i
RUN npm run build

RUN adduser app --disabled-password
USER app

EXPOSE 3000
ENV NODE_ENV=production

CMD [ "node", "build/index.js" ]