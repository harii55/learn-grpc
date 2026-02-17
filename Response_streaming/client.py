import grpc
import asyncio
import os
import sys
import yaml
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import helloworld_pb2
import helloworld_pb2_grpc

def load_config():

    load_dotenv()
    
    with open("../config.yml", "r") as f:
        config_content = f.read()
    
    # Substitute environment variables in config.yml
    config_content = os.path.expandvars(config_content)
    
    return yaml.safe_load(config_content)
async def run():
    config = load_config()
    port = config.get("port")

    async with grpc.aio.insecure_channel(f'localhost:{port}') as channel:
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
