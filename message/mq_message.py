#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   Untitled-1
@Time    :   2020/06/24 14:20:54
@Author  :   taoleilei 
@Version :   1.0
@Contact :   taoleilei6176@163.com
@License :   (C)Copyright 2019-2020
@Desc    :   None
'''

import json
import logging
import os
import random
import shutil
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

import pymysql
import stomp
from DBUtils.PooledDB import PooledDB
from stomp.exception import StompException

ACTIVEMQ = {
    "HOST": '192.168.125.72',
    "PORT": '32802',
    "USER": "admin",
    "PASSWORD": "admin",
    "SEND": 'UI2MCUMessageTopic',
    "RECV": 'MCU2UIMessageTopic',
    "TYPE": "topic"
}
DATABASES = {
    "host": "192.168.131.199",
    "port": 3306,
    "user": "root",
    "passwd": "iiecas",
    "db": "x",
    'charset': 'utf8',
}
LOG_PATH = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "message.log")
print(LOG_PATH)


def logs_initial():
    handler = logging.FileHandler(LOG_PATH, 'a', encoding='utf-8')
    fmt = logging.Formatter(
        fmt="%(asctime)s  %(name)s  %(levelname)s  %(module)s:  %(message)s")
    handler.setFormatter(fmt)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger


logger = logs_initial()


class SQLPoll():
    __poll = None

    def __init__(self):
        self.pool = self.__get_db()
        self.conn = self.pool.connection()
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    @classmethod
    def __get_db(cls):
        if cls.__poll is None:
            cls.__poll = PooledDB(
                creator=pymysql,
                mincached=10,
                maxconnections=100,
                **DATABASES)
        return cls.__poll

    def fetch_all(self, sql, args=None):
        if args is None:
            self.cursor.execute(sql)
        else:
            self.cursor.execute(sql, args)
        result = self.cursor.fetchall()
        return result

    def fetch_one(self, sql, args=None):
        if args is None:
            self.cursor.execute(sql)
        else:
            self.cursor.execute(sql, args)
        result = self.cursor.fetchone()
        return result

    def execute(self, sql, args):
        self.cursor.execute(sql, args)
        self.conn.commit()
        result = self.cursor.lastrowid
        return result

    def __close(self):
        self.cursor.close()
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__close()


class CallbackHandle():
    """docstring for CallbackHandler"""

    def __init__(self):
        pass

    @staticmethod
    def msg_normalize(message):
        try:
            message = json.loads(message)
        except Exception as e:
            raise e

        return message

    def handle_deploy(self, message):
        print("received deploy message\n %s" % message)
        logger.info(message)

    def handle_start(self, message):
        print("received start message\n %s" % message)
        logger.info(message)

    def handle_close(self, message):
        print("received close message\n %s" % message)
        logger.info(message)

    def handle_default(self, message):
        print("received message\n %s" % message)
        logger.info(message)

    def handle_general(self, message):
        print("handle_general")
        # sql_one = '''
        #     UPDATE b_topic_task
        #     SET recv_msg = %s,
        #     state = %s,
        #     web_status = %s,
        #     recv_time = now(),
        #     feedback_emsg = %s,
        #     downfile = %s,
        #     duration = timestampdiff( SECOND, send_time, now( ) )
        #     WHERE
        #         taskid = %s
        # '''
        # taskid = message['taskid']
        # result = message['result']
        # conclusion = result['conclusion']
        # feedback_emsg = result.get('emessage', '')
        # downfile = result.get('feedInfo', '')

        # state = 2 if conclusion == 1 else 1
        # web_status = 1 if conclusion == 1 else 2
        # with SQLPoll() as db:
        #     db.execute(sql_one, (json.dumps(message), state,
        #                          web_status, feedback_emsg, downfile, taskid))


callback = CallbackHandle()


class MyListener(stomp.ConnectionListener):
    def __init__(self, conn, headers):
        super().__init__()
        self.conn = conn
        self.headers = headers

    def on_error(self, headers, message):
        print('received an error %s' % message)
        logger.error('received an error %s' % message)

    def on_message(self, headers, message):
        print('--------------------------------------')
        normal_data = callback.msg_normalize(message)
        handler = "handle_{}".format(normal_data["name"].lower())
        if hasattr(callback, handler):
            callback.handle_general(normal_data)
            method = getattr(callback, handler)
            method(normal_data)
        elif hasattr(callback, "handle_default"):
            method = getattr(callback, "handle_default")
            method(normal_data)

        # print('received message\n %s' % normal_data)

    def on_disconnected(self):
        """
        Called by the STOMP connection when a TCP/IP connection to the STOMP server has been lost.  No messages should be sent via the connection until it has been reestablished.
        """
        print('Error: conn failure!')
        print('+++++++++++++++++++++++++++++++++++++++++++')

    def on_connecting(self, host_and_port):
        """
        Called by the STOMP connection once a TCP/IP connection to the STOMP server has been established or re-established. Note that at this point, no connection has been established on the STOMP protocol level. For this, you need to invoke the "connect" method on the connection.

        :param host_and_port: a tuple containing the host name and port number to which the connection has been established.
        """
        print("%s %s on connecting" % host_and_port)
        logger.info("%s %s on connecting" % host_and_port)

    def on_connected(self, headers, body):
        """
        Called by the STOMP connection when a CONNECTED frame is
        received, that is after a connection has been established or re-established.

        :param headers: a dictionary containing all headers sent by the server as key/value pairs.

        :param body: the frame's payload. This is usually empty for CONNECTED frames.
        """
        print(headers)
        print(body)
        print("on connected")
        logger.info(body)
        logger.info("on connected")

    def on_heartbeat_timeout(self):
        """
        Called by the STOMP connection when a heartbeat message has not been received beyond the specified period.
        """
        print("on heartbeat timeout")

    def on_receipt(self, headers, body):
        """
        Called by the STOMP connection when a RECEIPT frame is
        received, sent by the server if requested by the client using
        the 'receipt' header.

        :param headers: a dictionary containing all headers sent by the server as key/value pairs.

        :param body: the frame's payload. This is usually empty for RECEIPT frames.
        """
        print(headers)
        print(body)
        print("on receipt")


class BaseError(Exception):
    """ 自定义异常基类 """

    def __init__(self, code):
        super().__init__(code)
        self.code = code


class ConnectionError(BaseError):
    """ 连接异常类 """


class MQMessageHandler():
    """ MQ连接建立类 """

    def __init__(self, **kwargs):
        self.id = random.randint(1, 1000)
        for key, value in kwargs.items():
            setattr(self, key.lower(), value)

        self.address = (self.host, self.port)
        self.topic = "/%s/%s" % (self.type, self.recv)
        self.headers = {'tcpNoDelay': 'true'}

    def _connect(self):
        self.conn = stomp.Connection([self.address], auto_content_length=False)
        print('set up Connection')
        logger.info('set up Connection')

    def _disconnect(self):
        self.conn.unsubscribe(self.id)
        self.conn.disconnect()
        print("disconnected")
        logger.info("disconnected")

    def listener(self):
        # 监听者
        self.conn.set_listener('', MyListener())
        print('Set up listener')
        logger.info('Set up listener')

        self.conn.connect(self.user, self.password,
                          wait=True, headers=self.headers)
        print('started connection')
        logger.info('started connection')

        self.conn.subscribe(destination=self.topic, id=self.id, ack='auto')
        print(f'subscribed {self.topic}')
        logger.info(f'subscribed {self.topic}')
        while True:
            time.sleep(1)

    def __enter__(self):
        self._connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if self.conn.is_connected():
                self._disconnect()
        except Exception as e:
            pass

        if issubclass(exc_type, StompException):
            print("发送邮件...")
            logger.info("发送邮件...")
            # sys.exit(1)
            raise ConnectionError(500)


if __name__ == '__main__':
    try:
        p = Path(LOG_PATH)
        if p.exists():
            # p.resolve()
            pass
        count = 3
        while count:
            try:
                with MQMessageHandler(**ACTIVEMQ) as handler:
                    handler.listener()
            except ConnectionError:
                print("连接失败，等待5秒重新连接")
                logger.error("连接失败，等待5秒重新连接")
                count -= 1
                if count:
                    time.sleep(5)
            except Exception as e:
                break
        else:
            print("连接无效")
            logger.error("连接无效")
    except KeyboardInterrupt as e:
        print("进程终止")
        logger.info("进程终止")
        sys.exit(0)
