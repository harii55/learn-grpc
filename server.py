import grpc
import importlib
import helloworld_pb2_grpc
import asyncio
import signal


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
        
        # Setup signal handlers for graceful shutdown
        loop = asyncio.get_event_loop()
        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(sig, lambda: asyncio.create_task(self.stop()))
        
        await self.server.wait_for_termination()

    async def stop(self):
        if self.server:
            print("\nShutting down server gracefully...")
            await self.server.stop(grace=2)
            print("Server stopped")


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


