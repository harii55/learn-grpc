import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import grpc
import asyncio
import helloworld_pb2
import helloworld_pb2_grpc

async def run():
    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)
              
        request = helloworld_pb2.HelloRequest(name='Carly')

        response_stream = stub.SayHelloStreamReply(request)

        while True:
            response = await response_stream.read()
            if response == grpc.aio.EOF:
                break
            print("Client just received this: " + response.message)


if __name__ == "__main__":
    asyncio.run(run())
