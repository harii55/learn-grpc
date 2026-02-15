import grpc
import importlib
import helloworld_pb2_grpc
import sys
import asyncio


class Server:
    def __init__(self, servicer_class, port):
        self.servicer_class = servicer_class
        self.port = port
        self.server = None


    async def start(self):
        # Start the gRPC server with provided servicer
        self.server = grpc.aio.server()
        
        servicer_instance = self.servicer_class()
        helloworld_pb2_grpc.add_GreeterServicer_to_server(servicer_instance, self.server)
        self.server.add_insecure_port(f'[::]:{self.port}')
        await self.server.start()
        print(f"Server started with {self.servicer_class.__name__} on port {self.port}")
        
        await self.server.wait_for_termination()

    async def stop(self):
        if self.server:
            await self.server.stop(grace=5)


def load_servicer(module_path, class_name):
        try:
            module = importlib.import_module(module_path)
            servicer_class = getattr(module, class_name)
            return servicer_class
        except (ImportError, AttributeError) as e:
            raise ImportError(f"Failed to load {class_name} from {module_path}: {e}")
        

async def run_server(module_path, class_name, port):
        servicer = load_servicer(module_path, class_name)
        runner = Server(servicer, port)
        await runner.start()


if __name__ == "__main__":
    # Example: python server_runner.py Simple-RPC.servicer UnaryServicer 50051
    if len(sys.argv) != 4:
        print("Usage: python server_runner.py <module> <class> <port>")
        sys.exit(1)
    
    module = sys.argv[1]
    cls = sys.argv[2]
    port = sys.argv[3]
    
    asyncio.run(run_server(module, cls, port))


