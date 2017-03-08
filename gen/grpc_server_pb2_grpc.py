import grpc

import grpc_server_pb2 as grpc__server__pb2


class PositionServerStub(object):
    def __init__(self, channel):
        """Constructor.
    
        Args:
          channel: A grpc.Channel.
        """
        self.registerClient = channel.unary_unary(
            '/opencv_object_tracking.PositionServer/registerClient',
            request_serializer=grpc__server__pb2.ClientInfo.SerializeToString,
            response_deserializer=grpc__server__pb2.ServerInfo.FromString,
        )
        self.getPositions = channel.unary_stream(
            '/opencv_object_tracking.PositionServer/getPositions',
            request_serializer=grpc__server__pb2.ClientInfo.SerializeToString,
            response_deserializer=grpc__server__pb2.Position.FromString,
        )


class PositionServerServicer(object):
    def registerClient(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getPositions(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_PositionServerServicer_to_server(servicer, server):
    rpc_method_handlers = {
        'registerClient': grpc.unary_unary_rpc_method_handler(
            servicer.registerClient,
            request_deserializer=grpc__server__pb2.ClientInfo.FromString,
            response_serializer=grpc__server__pb2.ServerInfo.SerializeToString,
        ),
        'getPositions': grpc.unary_stream_rpc_method_handler(
            servicer.getPositions,
            request_deserializer=grpc__server__pb2.ClientInfo.FromString,
            response_serializer=grpc__server__pb2.Position.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        'opencv_object_tracking.PositionServer', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
