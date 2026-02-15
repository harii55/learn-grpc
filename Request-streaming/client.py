import grpc
import asyncio
import os
import sys
import yaml

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import helloworld_pb2
import helloworld_pb2_grpc

def load_config():
    with open("../config.yml", "r") as f:
        return yaml.safe_load(f)

async def run():

    async def generate_msg():
        for i in range(5):
            print(f"Sent this name via req: Carly {i}")
            yield helloworld_pb2.HelloRequest(
                name = f"Carly {i}"
            )
            await asyncio.sleep(1)


    config = load_config()
    port = config['services']['service-3']['port']

    async with grpc.aio.insecure_channel(f'localhost:{port}') as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)

        req_iter = generate_msg()

        res = await stub.SayHelloStreamRequest(req_iter)


        print(res.message)


if __name__ == "__main__":
    asyncio.run(run())

        