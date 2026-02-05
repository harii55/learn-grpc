import os,sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import grpc
import asyncio
import helloworld_pb2
import helloworld_pb2_grpc
from typing import AsyncIterable

class RequestStreamingServicer(helloworld_pb2_grpc.GreeterServicer):
    
    async def SayHelloStreamRequest(self, request_iterator: AsyncIterable[helloworld_pb2.HelloRequest], context
                                    )->helloworld_pb2.HelloReply:
        counter=0 
        async for items in request_iterator:
            print(f"Received request from: {items.name}")
            counter += 1

        return helloworld_pb2.HelloReply(message=f"Hello, {counter} Requests received! This is the final response after processing all requests.")
           


async def server():
    port="50051"
    server=grpc.aio.server()

    helloworld_pb2_grpc.add_GreeterServicer_to_server(RequestStreamingServicer(),server)

    server.add_insecure_port(f'[::]:{port}')
    await server.start()

    print(f"Responce Streaming Server started, listening on {port}")

    await server.wait_for_termination()

if __name__ == "__main__":
    asyncio.run(server())