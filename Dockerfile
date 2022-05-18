ARG DOCKER_REGISTRY=public.docker.shared.op
FROM ${DOCKER_REGISTRY}/base/python:3.8 as build
ARG PIP_INDEX_URL=http://public.nexus.shared.op/repository/pypi-hosted/simple/
ARG PIP_INDEX_HOST=public.nexus.shared.op

WORKDIR /app

COPY setup.py .
COPY requirements.txt .
COPY model_parser ./model_parser
ENV PIP_INDEX_URL=${PIP_INDEX_URL}
RUN python3 -m venv --system-site-packages venv && \
    . venv/bin/activate && \
    pip install --no-cache-dir --trusted-host ${PIP_INDEX_HOST} -U pip && \
    pip install --no-cache-dir --trusted-host ${PIP_INDEX_HOST} sphinx sphinx-rtd-theme && \
    pip install --no-cache-dir --trusted-host ${PIP_INDEX_HOST} -r requirements.txt && \
    sphinx-quickstart -q --sep \
    --project model_parser \
    --author nil \
    --language html \
    --ext-autodoc \
    --ext-doctest && \
    sphinx-apidoc -o source model_parser && \
    cat source/conf.py | sed -e "s/# import/import/g" | sed -e "s/# sys.path/sys.path/g" | sed -e "s/'\.'/'\.\.\/\.'/g" | sed -e "s/alabaster/sphinx_rtd_theme/g" | tee source/conf_new.py && \
    cat source/index.rst | sed -e 's/Contents\:/Contents\:\n\n   modules/' | tee source/index_new.rst && \
    mv source/conf_new.py source/conf.py && \
    mv source/index_new.rst source/index.rst && \
    make html

ARG DOCKER_REGISTRY=public.docker.shared.op
FROM ${DOCKER_REGISTRY}/base/nginx:1.21.3

COPY --from=build /app/build/html /usr/share/nginx/html

RUN echo 'server {' > /etc/nginx/conf.d/default.conf && \ 
    echo '  listen 80;' >> /etc/nginx/conf.d/default.conf && \ 
    echo '  location / {' >> /etc/nginx/conf.d/default.conf && \ 
    echo '    root /usr/share/nginx/html;' >> /etc/nginx/conf.d/default.conf && \ 
    echo '    index index.html index.htm;' >> /etc/nginx/conf.d/default.conf && \ 
    echo '    try_files $uri $uri/ /index.html =404;' >> /etc/nginx/conf.d/default.conf && \ 
    echo '  }' >> /etc/nginx/conf.d/default.conf && \ 
    echo '}' >> /etc/nginx/conf.d/default.conf

EXPOSE 80
ENTRYPOINT ["nginx", "-g", "daemon off;"]
