import os,sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import grpc
import asyncio
import helloworld_pb2
import helloworld_pb2_grpc

# dependent stream: client will send names with 1 sec timeout , server need to send reply msg for every name/req as soon as it arrives 
# independent stream: server will send 1 to 10 with delay of 2 sec each.

# will need queue.
 

class BidirectionalStreamingServicer(helloworld_pb2_grpc.GreeterServicer):

    async def SayHelloBidiStream(self, request_iterator, context):

        response_queue = asyncio.Queue()

        async def independent_stream():
            for i in range(1,11):
                print(f"Independent stream : Sent {i}")
                await response_queue.put(
                    helloworld_pb2.HelloReply(message=f"Independent stream : Sent {i}")
                )
                await asyncio.sleep(2)

        async def dependent_stream():
            async for req in request_iterator:
                print(f"Received request from: {req.name}")
                await response_queue.put(
                    helloworld_pb2.HelloReply(message=f"Dependent stream : Hello {req.name}!")
                )
            await response_queue.put(None)  
            # Why put None here?
            # Coz the client is done sending messages (stream ended or disconnected).
            # We need to break the main loop! -> Put None.

            

        task1 = asyncio.create_task(independent_stream())
        task2 = asyncio.create_task(dependent_stream())

        
        while True:
            res = await response_queue.get()

            if res is None:
                break

            yield res

        task1.cancel()
        # Why cancel task1 here?
        # If the client disconnects early (e.g. after 5 sec), the loop above breaks.
        # But task1 might still be running in the background (trying to count to 10).
        # We must FORCE STOP it so it doesn't become a zombie task eating up RAM.
        # (If task1 was already finished, this line does nothing, so it's safe).


async def server():
    port="50051"
    server=grpc.aio.server()

    helloworld_pb2_grpc.add_GreeterServicer_to_server(BidirectionalStreamingServicer(),server)

    server.add_insecure_port(f'[::]:{port}')
    await server.start()

    print(f"Responce Streaming Server started, listening on {port}")

    await server.wait_for_termination()

if __name__ == "__main__":
    asyncio.run(server())







# Why Need Queue? 

# Coz : you cant use yield two times in the same stream : asynchronously

# class BidirectionalStreamingServicer(helloworld_pb2_grpc.GreeterServicer):
    # async def SayHelloBidiStream(self, request_iterator, context):
    #     async for req in request_iterator:
    #         print(f"Received request from: {req.name}")
    #         yield helloworld_pb2.HelloReply(message=f"Hello, {req.name}!")

    #     async for i in range(1, 11):
    #             yield helloworld_pb2.HelloReply(message=f"Independent Stream Message: {i}")
    #             await asyncio.sleep(2)

    



async def server():
    port="50051"
    server=grpc.aio.server()

    helloworld_pb2_grpc.add_GreeterServicer_to_server(BidirectionalStreamingServicer(),server)

    server.add_insecure_port(f'[::]:{port}')
    await server.start()

    print(f"Responce Streaming Server started, listening on {port}")

    await server.wait_for_termination()

if __name__ == "__main__":
    asyncio.run(server())
       


