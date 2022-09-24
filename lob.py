import json
import multiprocessing
import time
import pandas as pd
from multiprocessing import Process
from websocket import create_connection
from tree import AVL, Level


def kraken():
    ws = create_connection('wss://ws.kraken.com/')
    ws.send(json.dumps({
        "event": "subscribe",
        "pair": ["DOT/USD"],
        "subscription": {"name":"book"}
    }))


    while True:
        result = ws.recv()
        result = json.loads(result)
        q.put(result)


class Book:
    def __init__(self, bids, asks, rta, rtb):
        self.bids = bids
        self.asks = asks
        self.rta = rta
        self.rtb = rtb

    def insert(self, load):
        if list(load.keys())[0] == 'a':
            for i in load['a']:
                order = Level(float(i[0]),float(i[1]),i[2])
                if order.size > 0:
                    self.rta = self.asks.insert(order, self.rta)
                else:
                    self.rta = self.asks.delete(order, self.rta)
        elif list(load.keys())[0] == 'b':
            for i in load['b']:
                order = Level(float(i[0]),float(i[1]),i[2])
                if order.size > 0:
                    self.rtb = self.bids.insert(order, self.rtb)
                else:
                    self.rtb = self.bids.delete(order, self.rtb)

    def init_book(self, load):
        for i in load['as']:
            order = Level(float(i[0]),float(i[1]),i[2])
            self.rta = self.asks.insert(order, self.rta)
        for i in load['bs']:
            order = Level(float(i[0]),float(i[1]),i[2])
            self.rtb = self.bids.insert(order, self.rtb)

    def request_book(self):
        bids = self.bids.inorderTraversal(self.rtb)
        asks = self.asks.inorderTraversal(self.rta)
        return bids, asks


def consumerProcess(q, book):
    while True:
        load = q.get()
        if type(load) == list:
            if list(load[1].keys())[0] == 'as':
                book.init_book(load[1])
            elif list(load[1].keys())[0] in ['a', 'b']:
                book.insert(load[1])
            else:
                pass

def consumerProcess2(q):
    dict = {}
    while True:
        load = q.get()
        bids, asks = load.request_book()
        bid_s = []
        bid_l = []
        ask_l = []
        ask_s = []
        for i in bids:
            bid_l.append(i.price)
            bid_s.append(i.size)
        for i in asks:
            ask_l.append(i.price)
            ask_s.append(i.size)
        bid_l.reverse()
        bid_s.reverse()
        dict['size bid'] = bid_s[:5]
        dict['bids'] = bid_l[0:5]
        dict['asks'] = ask_l[0:5]
        dict['size ask'] = ask_s[0:5]
        df = pd.DataFrame(dict)
        print(df)
        time.sleep(7)


if __name__=='__main__':

    bids = AVL()
    asks = AVL()
    rta = None
    rtb = None
    book = Book(bids, asks, rta, rtb)

    multiprocessing.set_start_method = "fork"
    q = multiprocessing.Queue(maxsize=40)
    p1 = Process(target = kraken)
    p1.start()
    print(book)
    p2 = consumerProcess = multiprocessing.Process(target=consumerProcess, args=(q,book))
    p2.start()



