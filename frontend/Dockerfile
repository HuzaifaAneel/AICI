FROM node:18-alpine AS build

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm install

COPY . .

RUN npm run build

FROM node:18-alpine

RUN npm install -g serve

COPY --from=build /app/build /usr/share/build

EXPOSE 3000

CMD ["serve", "-s", "/usr/share/build", "-l", "3000"]
