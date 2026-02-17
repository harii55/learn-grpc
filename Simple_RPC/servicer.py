import helloworld_pb2
import helloworld_pb2_grpc
import grpc

class UnaryServicer(helloworld_pb2_grpc.GreeterServicer):
   
    async def SayHello(self, request, context: grpc.aio.ServicerContext):

        # client will send a request with a name, and we will print it on the server side, and send hello name back to client.
        print(f"Received request from: {request.name}")

        
        return helloworld_pb2.HelloReply(
            message=f"Hello, {request.name}!")
    

