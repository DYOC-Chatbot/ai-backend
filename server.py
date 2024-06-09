from concurrent import futures
import logging
import os

import grpc
import ai_service_pb2
import ai_service_pb2_grpc

from use_model import predict_message

from dotenv import load_dotenv

load_dotenv(".env")
PORT = os.getenv("PORT")
if PORT == None:
    PORT = "50051"


class AIService(ai_service_pb2_grpc.AIServiceServicer):
    def ClassifyType(self, request: ai_service_pb2.ClassifyTypeRequest, context):
        message_type = predict_message(request.message)
        return ai_service_pb2.ClassifyTypeReply(
            type=ai_service_pb2.MESSAGE_QUERY if message_type == "Query" else ai_service_pb2.MESSAGE_REQUEST
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ai_service_pb2_grpc.add_AIServiceServicer_to_server(AIService(), server)
    server.add_insecure_port("[::]:" + PORT)
    server.start()
    print("Server started, listening on " + PORT)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()
