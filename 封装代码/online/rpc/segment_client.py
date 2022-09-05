import grpc

from online.rpc.segment_pb2 import SegRequest, AddWordRequest, DeleteWordRequest  # 引入Request类
from online.rpc.segment_pb2_grpc import SegmentStub  # 引入stub，和服务端交互


class SegmentClient(object):
    """
    客户端代码，提供给使用方直接import使用

    作用：
        定义各种接口
        将原始函数输入封装为Request对象
        发送Request到server端，获得返回的Response
        解析Response对象为python基本类型，返回给用户
    """

    def __init__(self, host, port):
        """
        声明host, port 创建channel
        通过channel创建stub对象
        """
        channel = grpc.insecure_channel('{}:{}'.format(host, port))
        self.stub = SegmentStub(channel)

    def seg(self, content, model, enable_stop_word=False, use_ner=False):
        """定义seg接口"""
        # 将参数封装成request对象
        request = SegRequest(content=content, model=model, enable_stop_word=enable_stop_word,
                             use_ner=use_ner)

        # 调用stub.seg方法，传入request对象，得到response对象
        response = self.stub.seg(request)

        # 将response对象解析成list of tuple，返回给用户
        words = [(term.word, term.start_index, term.end_index) for term in response.terms]

        return words

    def pos(self, content, model, enable_stop_word=False, use_ner=False):
        """定义pos接口"""
        request = SegRequest(content=content, model=model, enable_stop_word=enable_stop_word,
                             use_ner=use_ner)
        response = self.stub.pos(request)
        words = [(term.word, term.start_index, term.end_index, term.pos) for term in response.terms]
        return words

    def add_word(self, word, pos, freq):
        """定义add_word接口"""
        request = AddWordRequest(word=word, pos=pos, freq=freq)
        response = self.stub.add_word(request)
        status = response.status
        return status

    def delete_word(self, word):
        """定义delete_word接口"""
        request = DeleteWordRequest(word=word)
        response = self.stub.delete_word(request)
        status = response.status
        return status
