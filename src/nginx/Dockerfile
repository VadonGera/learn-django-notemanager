# Используем официальный образ Nginx как базовый
FROM nginx:latest

# Удаляем стандартный конфигурационный файл Nginx
RUN rm /etc/nginx/conf.d/default.conf

# Копируем собственный конфигурационный файл в контейнер
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Создаем директорию для логов
RUN mkdir -p /var/log/nginx

# Указываем рабочую директорию, где будет доступ к статическим файлам
WORKDIR /my_application