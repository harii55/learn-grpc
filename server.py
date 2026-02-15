import grpc
import helloworld_pb2_grpc
import asyncio
import signal


class Server:
    def __init__(self, servicer_obj, port):
        self.servicer_obj=servicer_obj
        self.port = port
        self.server = None


    async def start(self):
        # Start the gRPC server with provided servicer
        self.server = grpc.aio.server()
        
        helloworld_pb2_grpc.add_GreeterServicer_to_server(self.servicer_obj, self.server)
        self.server.add_insecure_port(f'[::]:{self.port}')
        await self.server.start()
        print(f"Server started with {self.servicer_obj.__class__.__name__} on port {self.port}")   
             
        # Setup signal handlers for graceful shutdown
        loop = asyncio.get_event_loop()
        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(sig, lambda: asyncio.create_task(self.stop()))
        
        await self.server.wait_for_termination()

    async def stop(self):
        if self.server:
            print("\nShutting down server gracefully...")
            await self.server.stop(grace=3)
            print("Server stopped")
