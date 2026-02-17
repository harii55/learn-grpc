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

    # create a channel to the server
    async with grpc.aio.insecure_channel(f'localhost:{port}') as channel:
 
        # create a stub (client)
        stub = helloworld_pb2_grpc.GreeterStub(channel)

        # create a valid request message
        request = helloworld_pb2.HelloRequest(name='Carly')

        # make the call
        response = await stub.SayHello(request)

    print(f"Greeter client received: {response.message}")

if __name__ == "__main__":
    asyncio.run(run())