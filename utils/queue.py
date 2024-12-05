class HistoryQueue(list):
    def __init__(self, window_size=10, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.window_size = window_size

    def append(self, *args, **kwargs):
        super().append(*args, **kwargs)
        self.cut()

    def extend(self, *args, **kwargs):
        super().extend(*args, **kwargs)
        self.cut()
       
    def cut(self):
         while len(self) > self.window_size:
            for message in self:
                if message["role"] == "user":
                    self.pop(0) # pop user的提问
                    self.pop(0) # pop 模型的回答
                    break