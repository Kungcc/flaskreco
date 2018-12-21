FROM nginx

RUN mv /etc/nginx/nginx.conf /etc/nginx/nginx.conf.bk
COPY nginx.conf /etc/nginx/

RUN mv /etc/nginx//conf.d/default.conf /etc/nginx//conf.d/default.conf.bk
COPY flaskreco.conf /etc/nginx/conf.d/