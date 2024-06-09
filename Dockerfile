FROM python:3

RUN adduser app && adduser --gecos --system app app

USER app
WORKDIR /app

COPY requirements.txt ./

USER root
RUN chown -R app:app /app
RUN chmod -R 775 /app
USER app

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . .

RUN python -m grpc_tools.protoc -Iprotos --python_out=. --pyi_out=. --grpc_python_out=. --proto_path=protobuf protobuf/ai_service.proto

CMD python server.py