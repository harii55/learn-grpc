import helloworld_pb2
import helloworld_pb2_grpc
from typing import AsyncIterable


class RequestStreamingServicer(helloworld_pb2_grpc.GreeterServicer):
    
    async def SayHelloStreamRequest(self, request_iterator: AsyncIterable[helloworld_pb2.HelloRequest], context
                                    )->helloworld_pb2.HelloReply:
        counter=0 
        async for items in request_iterator:
            print(f"Received request from: {items.name}")
            counter += 1

        return helloworld_pb2.HelloReply(message=f"Hello, {counter} Requests received! This is the final response after processing all requests.")
           

