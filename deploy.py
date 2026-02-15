from logging import config
import yaml
import asyncio
from server import Server
import sys

from Simple_RPC.servicer import UnaryServicer
from Response_streaming.servicer import ResponseStreamingServicer
from Request_streaming.servicer import RequestStreamingServicer
from Bidirectional_streaming.servicer import BidirectionalStreamingServicer

possible_grpc_deployments = {
    "unary": UnaryServicer,
    "response_streaming": ResponseStreamingServicer,
    "request_streaming": RequestStreamingServicer,
    "bidi_streaming": BidirectionalStreamingServicer
}

def load_config():
    with open("config.yml", "r") as f:
        return yaml.safe_load(f)
    
async def deploy_service(servicer_obj, port, identity):
    
    print(f"Deploying {identity} on port {port}...")

    try:
        runner = Server(servicer_obj, port)
        await runner.start()
    except asyncio.CancelledError:
        await runner.stop()

def main():
    config = load_config()
    
    identity = config.get("identity")    
    servicer_class = possible_grpc_deployments.get(identity)

    if not servicer_class:
        print(f"Error: Identity '{identity}' not found in registry.")
        sys.exit(1)

    servicer_obj = servicer_class()

    asyncio.run(deploy_service(servicer_obj, config.get("port"), identity))


if __name__ == "__main__":
    main()