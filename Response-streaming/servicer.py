import asyncio
import grpc
import helloworld_pb2
import helloworld_pb2_grpc

# from helloworld_pb2 import HelloRequest, HelloReply

class ResponseStreamingServicer(helloworld_pb2_grpc.GreeterServicer):
    
    async def SayHelloStreamReply(self, request: helloworld_pb2.HelloRequest, context: grpc.aio.ServicerContext) -> helloworld_pb2.HelloReply:
        print(f"Received request from: {request.name}")
        for i in range(5):
            await asyncio.sleep(1)  # Simulate some delay bw every reply.
            yield helloworld_pb2.HelloReply(
                message=f"Hello, {request.name}! This is message {i+1}.")
            


