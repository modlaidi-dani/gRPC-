import grpc
from .protos.serveur_resive_pb2_grpc import AgeServiceServicer, add_AgeServiceServicer_to_server 
from .protos.serveur_resive_pb2 import UserResponse
from concurrent import futures

class AgeService(AgeServiceServicer):
    def GetUser(self,request,context):
        age=request.age
        if age<18:
            category='mineur'
        else:
            category='major'
        response = UserResponse(username=request.email, category=category)
        return response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_AgeServiceServicer_to_server(AgeService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()    
    