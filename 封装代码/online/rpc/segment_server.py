import sys
import time
from concurrent import futures

import grpc

from online import logger
from online.rpc import segment_pb2_grpc
from online.rpc.segment_pb2 import SegResponse, PosResponse, Bool
from segment.segment import Segment


class SegmentServicer(segment_pb2_grpc.SegmentServicer):
    """
    服务端代码，服务端真实运行分词

    作用：
        定义客户端相应接口的响应
        得到Request对象，解析成python中的基本类型
        调用分词
        将分词结果封装为Response对象，返回给客户端
    """

    def __init__(self):
        """实例化segment对象，供后面调用"""
        self.segment = Segment()

    def seg(self, request, context):
        """处理seg请求"""
        # 解析Request对象为python基本类型的参数
        content, model, enable_stop_word, use_ner = \
            request.content, request.model, request.enable_stop_word, request.use_ner

        # 调用segment.seg，传入上面的参数，获得分词结果，并打印日志
        init_time = time.time()
        logger.info('seg for model: {}, enable_stop_word: {}, use_ner: {}, content: {} ...'.format(
            model, enable_stop_word, use_ner, content[:100]))
        words = list(self.segment.seg(content, model, enable_offset=True, enable_stop_word=enable_stop_word,
                                      use_ner=use_ner))
        logger.info('result: {}, cost_time: {}s'.format(words, time.time() - init_time))

        # 将分词结果封装为Response，返回给客户端
        response = SegResponse(
            terms=[
                SegResponse.Term(word=word, start_index=start_index, end_index=end_index)
                for word, start_index, end_index in words
            ]
        )
        return response

    def pos(self, request, context):
        """处理pos请求"""
        content, model, enable_stop_word, use_ner = \
            request.content, request.model, request.enable_stop_word, request.use_ner

        init_time = time.time()
        logger.info('pos for model: {}, enable_stop_word: {}, use_ner: {}, content: {} ...'.format(
            model, enable_stop_word, use_ner, content[:100]))
        words = list(self.segment.pos(content, model, enable_offset=True, enable_stop_word=enable_stop_word,
                                      use_ner=use_ner))
        logger.info('result: {}, cost_time: {}s'.format(words, time.time() - init_time))

        response = PosResponse(
            terms=[
                PosResponse.Term(word=word, start_index=start_index, end_index=end_index, pos=pos)
                for word, start_index, end_index, pos in words
            ]
        )
        return response

    def add_word(self, request, context):
        """处理add_word请求"""
        word, pos, freq = request.word, request.pos, request.freq

        logger.info('add_word for word: {}, pos: {}, freq: {}'.format(word, pos, freq))
        self.segment.add_word(word, pos, freq)

        response = Bool(status=True)
        return response

    def delete_word(self, request, context):
        """处理delete_word请求"""
        word = request.word

        logger.info('delete_word for word: {}'.format(word))
        self.segment.disable_word(word)

        response = Bool(status=True)
        return response


class SegmentServer(object):
    """
    定义SegmentServer
    设置host, port, workers，调用SegmentServicer
    """
    def __init__(self, port, max_workers):
        # 定义server对象，传入线程池、max_workers
        self.server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=max_workers), maximum_concurrent_rpcs=max_workers
        )

        # 将SegmentServicer添加到server
        segment_pb2_grpc.add_SegmentServicer_to_server(SegmentServicer(), self.server)

        # 设置server的host, port
        logger.info('rpc server starts with port: {}, max_workers: {}'.format(port, max_workers))
        self.server.add_insecure_port('0.0.0.0:{}'.format(port))

    def start(self):
        # 启动server
        self.server.start()
        while True:
            time.sleep(1e8)  # 主线程无限等


def start_server():
    port = 8000
    max_workers = 10

    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    if len(sys.argv) > 2:
        max_workers = int(sys.argv[2])

    server = SegmentServer(port, max_workers)
    server.start()


if __name__ == '__main__':
    start_server()
