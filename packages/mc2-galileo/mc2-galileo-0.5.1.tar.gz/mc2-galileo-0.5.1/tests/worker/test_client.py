import os
import threading
import time
import unittest
from queue import Queue
from typing import List

from pymq.provider.simple import SimpleEventBus
from symmetry.gateway import ServiceRequest
from timeout_decorator import timeout_decorator

from galileo.worker.api import ClientDescription, ClientConfig, SetWorkloadCommand
from galileo.worker.client import Client, RequestGenerator
from galileo.worker.context import Context, DebugRouter


class StaticRequestGenerator:

    def __init__(self, requests: List[ServiceRequest]) -> None:
        super().__init__()
        self.requests = requests

    def run(self):
        yield from self.requests

    def close(self):
        pass

    def set_rps(self, *args, **kwargs):
        pass


class ClientTest(unittest.TestCase):

    @timeout_decorator.timeout(5)
    def test_client_integration(self):
        env = dict(os.environ)
        env['galileo_router_type'] = 'DebugRouter'

        client_id = 'unittest_client'
        ctx = Context(env)
        trace_queue = Queue()

        description = ClientDescription(client_id, 'unittest_worker', ClientConfig('aservice'))
        # ctx: Context, trace_queue: Queue, description: ClientDescription

        client = Client(ctx, trace_queue, description, eventbus=SimpleEventBus())

        client.request_generator = StaticRequestGenerator([
            ServiceRequest('aservice'),
            ServiceRequest('aservice'),
        ])

        client.run()

        trace1 = trace_queue.get(timeout=2)
        trace2 = trace_queue.get(timeout=2)

        self.assertEqual('aservice', trace1.service)
        self.assertEqual('aservice', trace2.service)

        self.assertEqual('debughost', trace1.server)
        self.assertEqual('debughost', trace2.server)

        now = time.time()
        self.assertAlmostEqual(now, trace1.done, delta=2)
        self.assertAlmostEqual(now, trace2.done, delta=2)

    @timeout_decorator.timeout(5)
    def test_with_router_fault(self):
        class FaultInjectingRouter(DebugRouter):
            def request(self, req: ServiceRequest) -> 'requests.Response':
                if req.path == '/api/nonexisting':
                    raise ValueError('some error')

                return super().request(req)

        router = FaultInjectingRouter()

        ctx = Context()
        ctx.create_router = lambda: router
        client_id = 'unittest_client'
        trace_queue = Queue()

        description = ClientDescription(client_id, 'unittest_worker', ClientConfig('aservice'))
        # ctx: Context, trace_queue: Queue, description: ClientDescription

        client = Client(ctx, trace_queue, description, eventbus=SimpleEventBus())

        client.request_generator = StaticRequestGenerator([
            ServiceRequest('aservice', path='/api/nonexisting'),
            ServiceRequest('aservice', path='/api/unittest'),
        ])

        client.run()

        trace1 = trace_queue.get(timeout=2)
        trace2 = trace_queue.get(timeout=2)

        self.assertEqual(-1, trace1.sent)
        self.assertAlmostEqual(trace2.sent, time.time(), delta=2)


def queue_collect(vq: Queue, gen):
    for v in gen:
        vq.put(v)


class RequestGeneratorTest(unittest.TestCase):
    def test_with_limit_and_no_interval(self):
        workload = SetWorkloadCommand('myclient', 3)
        request_generator = RequestGenerator(lambda: 1)
        q = Queue()

        t = threading.Thread(target=queue_collect, args=(q, request_generator.run()))
        t.start()

        try:
            request_generator.set_workload(workload)
            self.assertEqual(1, q.get(timeout=1))
            self.assertEqual(1, q.get(timeout=1))
            self.assertEqual(1, q.get(timeout=1))
            self.assertEqual(RequestGenerator.DONE, q.get())
            self.assertEqual(0, q.qsize())
        finally:
            request_generator.close()
            t.join(2)

    def test_with_interval(self):
        workload = SetWorkloadCommand('myclient', parameters=(0.1,))  # 0.1 interarrival delay
        request_generator = RequestGenerator(lambda: 1)
        q = Queue()

        t = threading.Thread(target=queue_collect, args=(q, request_generator.run()))
        t.start()

        try:
            request_generator.set_workload(workload)
            time.sleep(2)
            self.assertAlmostEqual(20, q.qsize(), delta=3)
        finally:
            request_generator.close()
            t.join(2)

    def test_with_interval_and_limit(self):
        workload = SetWorkloadCommand('myclient', num=10, parameters=(0.05,))  # 0.05 interarrival delay
        request_generator = RequestGenerator(lambda: 1)
        q = Queue()

        t = threading.Thread(target=queue_collect, args=(q, request_generator.run()))
        t.start()

        try:
            request_generator.set_workload(workload)

            while True:
                item = q.get(timeout=2)
                if item is RequestGenerator.DONE:
                    break

            self.assertEqual(0, q.qsize())
        finally:
            request_generator.close()
            t.join(2)
