import grpc
import helloworld_pb2
import helloworld_pb2_grpc

def run():
    # create a channel to the server
    channel = grpc.insecure_channel('localhost:50051')

    with channel:   
        # create a stub (client)
        stub = helloworld_pb2_grpc.GreeterStub(channel)

        # create a valid request message
        request = helloworld_pb2.HelloRequest(name='Carly')

        # make the call
        response = stub.SayHello(request)

        print(f"Greeter client received: {response.message}")

if __name__ == "__main__":
    run()