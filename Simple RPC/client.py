import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import grpc
import helloworld_pb2
import helloworld_pb2_grpc
import asyncio

async def run():
    # create a channel to the server
    async with grpc.aio.insecure_channel('localhost:50051') as channel:
 
        # create a stub (client)
        stub = helloworld_pb2_grpc.GreeterStub(channel)

        # create a valid request message
        request = helloworld_pb2.HelloRequest(name='Carly')

        # make the call
        response = await stub.SayHello(request)

    print(f"Greeter client received: {response.message}")

if __name__ == "__main__":
    asyncio.run(run())