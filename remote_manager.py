 
def setup_remote_manager():
    queue = Queue()
    class QueueManager(BaseManager): pass
    QueueManager.register('get_queue', callable=lambda:queue)
    m = QueueManager(address=('', 5002))
    s = m.get_server()
    s.serve_forever()


if __name__ == "__main__":
    setup_remote_manager