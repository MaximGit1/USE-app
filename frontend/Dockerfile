FROM node:18

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

# Запуск сервера разработки (не для продакшена)
CMD ["npm", "run", "dev"]
