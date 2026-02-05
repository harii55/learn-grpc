import os,sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import grpc
import asyncio
import helloworld_pb2
import helloworld_pb2_grpc

async def run():

    async def generate_msg():
        for i in range(15):  # try with 10, 25 etc..
            print(f"Sent this name via req: Carly {i}")
            yield helloworld_pb2.HelloRequest(
                name = f"Carly {i}"
            )
            await asyncio.sleep(1)


    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)

        req_iter = generate_msg()

        res = stub.SayHelloBidiStream(req_iter)

        async for response in res:
            print("Client just received this: " + response.message)


if __name__== "__main__":
    asyncio.run(run())

