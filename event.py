# event.py (improved) https://emptypage.jp/notes/pyevent.en.html

class Event(object):
    
    def __init__(self, doc=None):
        self.__doc__ = doc
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return EventHandler(self, obj)
    
    def __set__(self, obj, value):
        pass


class EventHandler(object):
    
    def __init__(self, event, obj):
        
        self.event = event
        self.obj = obj
    
    def _getfunctionlist(self):
        
        """(internal use) """
        
        try:
            eventhandler = self.obj.__eventhandler__
        except AttributeError:
            eventhandler = self.obj.__eventhandler__ = {}
        return eventhandler.setdefault(self.event, [])
    
    def subscribe(self, func):
        
        """Add new event handler function.
        
        Event handler function must be defined like func(sender, earg).
        You can add handler also by using '+=' operator.
        """
        
        self._getfunctionlist().append(func)
        return self
    
    def unsubscribe(self, func):
        
        """Remove existing event handler function.
        
        You can remove handler also by using '-=' operator.
        """
        
        self._getfunctionlist().remove(func)
        return self
    
    def call(self, earg=None):
        
        """Fire event and call all handler functions
        
        You can call EventHandler object itself like e(earg) instead of 
        e.fire(earg).
        """
        
        for func in self._getfunctionlist():
            func(self.obj, earg)
    
    __iadd__ = subscribe
    __isub__ = unsubscribe
    __call__ = call

