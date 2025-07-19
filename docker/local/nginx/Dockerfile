FROM nginx:1.25.3-alpine

LABEL maintainer="api.vbm7752@gmail.com"
LABEL project="ecommerce"
LABEL description="Nginx setup for Django Ecommerce project"

# Remove default config
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom config
COPY default.conf /etc/nginx/conf.d/

# Static file directory (adjust path if needed)
RUN mkdir -p /staticfiles
