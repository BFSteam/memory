class news(dict):
    def __init__(self, *arg, **kw):
        super(news, self).__init__(*arg, **kw)
        self.init_vars()

    _news_parameters = [
        'id-n',
        'new',
        'id-source',
        'date-creation',
        'relevance',
    ]

    def __setitem__(self, key, item):
        print('setitem')
        if key not in self._news_parameters:
            return
        self.__dict__[key] = item

    def __getitem__(self, key):
        print('getitem')
        return self.__dict__[key]

    def __repr__(self):
        print('repr')
        return repr(self.__dict__)

    def __len__(self):
        print('len')
        return len(self.__dict__)

    def __delitem__(self, key):
        print('del')

        del self.__dict__[key]

    def clear(self):
        print('clear')
        self.init_vars()
        #return self.__dict__.clear()

    def copy(self):
        print('copy')
        return self.__dict__.copy()

    def has_key(self, k):
        print('haskey')
        return k in self.__dict__

    def update(self, *args, **kwargs):
        print('update was disabled for class news')
        #return self.__dict__.update(*args, **kwargs)

    def keys(self):
        print('keys')
        return self.__dict__.keys()

    def values(self):
        print('values')
        return self.__dict__.values()

    def items(self):
        print('items')
        return self.__dict__.items()

    def pop(self, *args):
        print('pop was disabled for news class')
        #return self.__dict__.pop(*args)

    def __cmp__(self, dict_):
        print('cmp')
        return self.__cmp__(self.__dict__, dict_)

    def __contains__(self, item):
        print('contains')
        return item in self.__dict__

    def __iter__(self):
        print('iter')
        return iter(self.__dict__)

    def __unicode__(self):
        print('unicode')
        return unicode(repr(self.__dict__))

    def init_vars(self):
        for n in news._news_parameters:
            self.__dict__[n] = None
