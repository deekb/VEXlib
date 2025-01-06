from .BinarySemaphore import BinarySemaphore


class SafeList:
    """
    A thread-safe wrapper for a list using BinarySemaphore to prevent simultaneous mutation/access.
    """

    def __init__(self):
        """
        Initializes the SafeList with an empty list and a BinarySemaphore.
        """
        self._list = []
        self._lock = BinarySemaphore()

    def _safe_method_call(self, method, *args, **kwargs):
        """
        Acquires the lock, executes the specified method with the given arguments,
        and then releases the lock.
        """
        self._lock.acquire()
        try:
            return method(*args, **kwargs)
        finally:
            self._lock.release()

    def append(self, item):
        """
        Appends an item to the list in a thread-safe manner.
        """
        self._safe_method_call(self._list.append, item)

    def remove(self, item):
        """
        Removes the first occurrence of the specified item from the list in a thread-safe manner.
        """
        self._safe_method_call(self._list.remove, item)

    def pop(self, index=-1):
        """
        Removes and returns the item at the specified index in a thread-safe manner.
        If no index is specified, removes and returns the last item in the list.
        """
        return self._safe_method_call(self._list.pop, index)

    def __getitem__(self, index):
        """
        Retrieves the item at the specified index in a thread-safe manner.
        Getitem is special in micropython and does not appear to work in the traditional "magic method" python way
        """
        self._lock.acquire()
        try:
            return self._list[index]
        finally:
            self._lock.release()

    def __setitem__(self, index, value):
        """
        Sets the item at the specified index to the given value in a thread-safe manner.
        """
        self._safe_method_call(self._list.__setitem__, index, value)

    def __len__(self):
        """
        Returns the number of items in the list in a thread-safe manner.
        """
        return self._safe_method_call(len, self._list)

    def __str__(self):
        """
        Returns a string representation of the list in a thread-safe manner.
        """
        return self._safe_method_call(str, self._list)

    def __bool__(self):
        """
        Returns True if the list is not empty, False otherwise.
        """
        return self._safe_method_call(bool, self._list)
