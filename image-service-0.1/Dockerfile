FROM python:3.9 AS builder

WORKDIR /usr/

RUN python3 -m venv ./venv
ENV PATH="/usr/venv/bin:$PATH"

WORKDIR /usr/src/dist

COPY ./dist/image_service-0.1-py3-none-any.whl ./image_service-0.1-py3-none-any.whl

RUN pip install image_service-0.1-py3-none-any.whl


FROM builder
WORKDIR /tmp
COPY --from=builder /usr/venv /venv
ENV PATH=/venv/bin:$PATH
