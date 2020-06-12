import threading

class AppThread(threading.Thread):
    def run(self):
        self._target()

def thread_func(*args):
    print('thread_running')
    print(args)


app_thread = AppThread(target=thread_func)

#app_thread.start()
app_thread.run()
