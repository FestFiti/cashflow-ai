FROM node:22-alpine

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install

COPY . .

ENV NODE_OPTIONS="--experimental-vm-modules"

EXPOSE 9999

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "9999"]
