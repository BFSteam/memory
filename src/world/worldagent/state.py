class state(list):
    # Read-only
    @property
    def maxLen(self):
        return self._maxLen

    def __init__(self, *args, **kwargs):
        self._maxLen = kwargs.pop("len")
        super(state, self).__init__(self, *args, **kwargs)

    def _truncate(self):
        """Called by various methods to reinforce the maximum length."""
        dif = len(self) - self._maxLen
        if dif > 0:
            #return
            self[:dif] = []

    def append(self, x):
        print('append was disabled for class state')
        #self.append(self, x)
        #self._truncate()

    def insert(self, *args):
        self.insert(self, *args)
        self._truncate()

    def extend(self, x):
        print('extend was disabled for class state')
        #self.extend(self, x)
        #self._truncate()

    def __setitem__(self, *args):
        self.__setitem__(self, *args)
        self._truncate()

    def __setslice__(self, *args):
        self.__setslice__(self, *args)
        self._truncate()
