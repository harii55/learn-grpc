import helloworld_pb2
import helloworld_pb2_grpc
import grpc
from concurrent import futures
import asyncio

class HelloWorldServicer(helloworld_pb2_grpc.GreeterServicer):
   
    async def SayHello(self, request, context: grpc.aio.ServicerContext):

        # client will send a request with a name, and we will print it on the server side, and send hello name back to client.
        print(f"Received request from: {request.name}")

        
        return helloworld_pb2.HelloReply(
            message=f"Hello, {request.name}!")
    


async def serve():
    # create a grpc server
    port="50051"
    server=grpc.aio.server()  

    # register the servicer
    helloworld_pb2_grpc.add_GreeterServicer_to_server(HelloWorldServicer(), server)

    # bind to port
    server.add_insecure_port(f'[::]:{port}')
    await server.start()

    print(f"Server started, listening on {port}")

    # keep the server running
    await server.wait_for_termination()

if __name__ == "__main__":
    asyncio.run(serve())