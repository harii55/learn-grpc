import asyncio
import grpc
import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)


import helloworld_pb2
import helloworld_pb2_grpc

# from helloworld_pb2 import HelloRequest, HelloReply

class HelloWorldStreamingServicer(helloworld_pb2_grpc.GreeterServicer):
    
    async def SayHelloStreamReply(self, request: helloworld_pb2.HelloRequest, context: grpc.aio.ServicerContext) -> helloworld_pb2.HelloReply:
        print(f"Received request from: {request.name}")
        for i in range(5):
            await asyncio.sleep(1)  # Simulate some delay bw every reply.
            yield helloworld_pb2.HelloReply(
                message=f"Hello, {request.name}! This is message {i+1}.")
            


async def server():
    port="50051"
    server=grpc.aio.server()

    helloworld_pb2_grpc.add_GreeterServicer_to_server(HelloWorldStreamingServicer(),server)

    server.add_insecure_port(f'[::]:{port}')
    await server.start()

    print(f"Responce Streaming Server started, listening on {port}")

    await server.wait_for_termination()

if __name__ == "__main__":
    asyncio.run(server())