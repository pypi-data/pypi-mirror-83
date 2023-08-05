"""
A deque, which is usually pronounced "deck", is a queue-like data structure
that supports insertion and deletion at both the front and the back of the
queue. Deque is a short for "double-ended queue". The deque is more general
than both the stack and the queue.

.. image:: ../../img/lists/deque.gif
"""
import warnings
from extra.lists.queue import Queue


class Deque(Queue):
    """
    A deque, which is usually pronounced "deck", is a queue-like data structure
    that supports insertion and deletion at both the front and the back of the
    queue. Deque is a short for "double-ended queue". The deque is more general
    than both the stack and the queue.
    """

    __name__ = "extra.Deque()"

    def __init__(self, max_capacity=float("inf")):
        """
        Creates a `Deque()` object!!

        Parameters
        ----------
        max_capacity: int
            It'dq a positive integer representing the maximum number of
            elements a `Deque()` should contain (Default: inf).

        Raises
        ------
        TypeError:
            If the type of `max_capacity` isn't `int` or `float`.
        ValueError:
            If the given value of `max_capacity` is less than zero.

        Example
        -------
        >>> dq = Deque()
        >>> type(dq)
        <class 'extra.lists.deque.Deque'>
        >>> dq._max_capacity
        inf

        You can define the maximum capacity for your own instance:

        >>> dq = Deque(10)
        >>> dq._max_capacity
        10

        Note
        ----
        If you passed a `float` number as the maximum capacity, then the value
        that get assigned is the rounding of that number:

        >>> dq = Deque(10.6)
        >>> dq._max_capacity
        11
        """
        super().__init__(max_capacity)

    # =============================     PRINT    ==============================
    def __repr__(self):
        """
        Represents the `Deque()` instance as a string.

        Returns
        -------
        str:
            The string-representation of the `Deque()` instance.

        Example
        -------
        >>> dq = Deque()
        >>> dq.append_left(10)
        >>> dq.append_left(20)
        >>> dq
        ─┬────┬────┬─
        ⟷│ 20 │ 10 │⟷
        ─┴────┴────┴─
        """
        return super()._print_queue("⟷")

    # =============================    LENGTH    ==============================
    def __len__(self):
        """
        Gets the length of the `Deque()` instance in constant time.

        Returns
        -------
        int:
            The length of the `Deque()` instance. By Length, I mean the number
            of nodes of in the instance.

        Examples
        --------
        >>> dq = Deque()
        >>> len(dq)
        0
        >>> dq.append_left(1)
        >>> dq.append_right(2)
        >>> dq.append_left(3)
        >>> len(dq)
        3
        """
        return super().__len__()

    def is_empty(self):
        """
        Checks if `Deque()` instance is empty or not in constant time.

        Returns
        -------
        bool:
            A boolean flag showing if the `Deque()` instance is empty or not.
            `True` shows that this instance is empty and `False` shows it's not
            empty.

        Example
        --------
        >>> dq = Deque()
        >>> dq.is_empty()
        True
        >>> dq.enqueue(5)
        >>> dq.is_empty()
        False
        """
        return super().is_empty()

    def is_full(self):
        """
        Checks if `Deque()` instance is at full-capacity in constant time.

        Returns
        -------
        bool:
            A boolean flag showing if the `Deque()` instance is full or not.
            `True` shows that this instance is full and `False` shows it's not
            full.

        Example
        --------
        >>> dq = Deque(max_capacity=2)
        >>> dq.is_full()
        False
        >>> dq.append_left(5)
        >>> dq.is_full()
        False
        >>> dq.append_right(10)
        >>> dq.is_full()
        True
        """
        return super().is_full()

    # =============================    APPEND    ==============================
    def append_left(self, item):
        """
        Inserts the given `item` to left-side of the `Deque()`, it does that in
        constant time.

        Parameters
        ----------
        item: object
            The python object to be pushed to the `Deque()`.

        Raises
        ------
        UserWarning:
            If the `Deque()` instance was full!! By "full", I mean the number
            of items in the `Deque()` equals to the assigned maximum capacity.
        ValueError:
            If the given `item` is `None`.
        TypeError:
            If the given `item` is an instance of `Extra`.

        Example
        -------
        >>> dq = Deque(max_capacity=2)
        >>> dq
        ─┬
        ⟷│
        ─┴
        >>> dq.append_left(1)
        >>> dq.append_left(2)
        >>> dq
        ─┬───┬───┬─
        ⟷│ 2 │ 1 │⟷
        ─┴───┴───┴─
        >>> dq.append_left(3)
        UserWarning: Enqueuing to a full `extra.Deque()` could lead to \
            missing values!!
        >>> dq
        ─┬───┬───┬─
        ⟷│ 3 │ 2 │⟷
        ─┴───┴───┴─

        Note
        ----
        This method does the same job as `Queue().enqueue`.
        """
        super().enqueue(item)

    def append_right(self, item):
        """
        Inserts the given `item` to right-side of the `Deque()`, it does that
        in constant time.

        Parameters
        ----------
        item: object
            The python object to be pushed to the `Deque()`.

        Raises
        ------
        UserWarning:
            If the `Deque()` instance was full!! By "full", I mean the number
            of items in the `Deque()` equals to the assigned maximum capacity.
        ValueError:
            If the given `item` is `None`.
        TypeError:
            If the given `item` is an instance of `Extra`.

        Example
        -------
        >>> dq = Deque(max_capacity=2)
        >>> dq
        ─┬
        ⟷│
        ─┴
        >>> dq.append_right(1)
        >>> dq.append_right(2)
        >>> dq
        ─┬───┬───┬─
        ⟷│ 1 │ 2 │⟷
        ─┴───┴───┴─
        >>> dq.append_right(3)
        UserWarning: Enqueuing to a full `extra.Deque()` could lead to \
            missing values!!
        >>> dq
        ─┬───┬───┬─
        ⟷│ 2 │ 3 │⟷
        ─┴───┴───┴─
        """
        super()._validate_item(item)
        if self.is_full():
            warnings.warn(
                f"Enqueuing to a full `{self.__name__}` "
                + "could lead to missing values!!",
                UserWarning,
            )
            self._container.remove_front()
        if self._max_capacity > 0:
            self._container._insert(len(self), item)

    # =============================      GET     ==============================
    def get_left(self):
        """
        Returns the left-most item of the `Deque()` instance in constant time.

        Returns
        -------
        object:
            The `Deque()` instance's left-most item.

        Raises
        ------
        IndexError:
            If the `Deque()` instance is empty!!

        Example
        -------
        >>> dq = Deque()
        >>> dq.top()
        IndexError: Can't retrieve from an empty `extra.Deque()`!!
        >>> dq.append_left(10)
        >>> dq.append_left(20)
        >>> dq
        ─┬────┬────┬─
        ⟷│ 20 │ 10 │⟷
        ─┴────┴────┴─
        >>> dq.get_left()
        20
        """
        if self.is_empty():
            raise IndexError(
                f"Can't retrieve from an empty `{self.__name__}`!!"
            )
        return self._container._head.get_data()

    def get_right(self):
        """
        Returns the right-most item of the `Deque()` instance in consant time.

        Returns
        -------
        object:
            The `Deque()` instance's right-most item.

        Raises
        ------
        IndexError:
            If the `Deque()` instance is empty!!

        Example
        -------
        >>> dq = Deque()
        >>> dq.top()
        IndexError: Can't retrieve from an empty `extra.Deque()`!!
        >>> dq.append_right(10)
        >>> dq.append_right(20)
        >>> dq
        ─┬────┬────┬─
        ⟷│ 10 │ 20 │⟷
        ─┴────┴────┴─
        >>> dq.get_right()
        20
        """
        return super().top()

    # =============================      POP     ==============================
    def pop_left(self):
        """
        Pops the left-most item from the `Deque()` in constant time.

        Returns
        -------
        object:
            The `Deque()` instance's left-most item.

        Raises
        ------
        UserWarning:
            If the `Deque()` instance is empty!!

        Example
        -------
        >>> dq = Deque()
        >>> dq.dequeue()
        UserWarning: Popping from empty `extra.Deque()`!!
        >>> dq.append_left(10)
        >>> dq.append_left(20)
        >>> dq
        ─┬────┬────┬─
        ⟷│ 20 │ 10 │⟷
        ─┴────┴────┴─
        >>> dq.pop_left()
        20
        >>> dq
        ─┬────┬─
        ⟷│ 10 │⟷
        ─┴────┴─
        """
        if self.is_empty():
            warnings.warn(f"Dequeuing from an empty `{self.__name__}`!!")
            return
        else:
            head_value = self._container._head.get_data()
            self._container.remove_front()
            return head_value

    def pop_right(self):
        """
        Pops the right-most item from the `Deque()` in constant time.

        Returns
        -------
        object:
            The `Deque()` instance's right-most item.

        Raises
        ------
        UserWarning:
            If the `Deque()` instance is empty!!

        Example
        -------
        >>> dq = Deque()
        >>> dq.dequeue()
        UserWarning: Popping from empty `extra.Deque()`!!
        >>> dq.append_right(10)
        >>> dq.append_right(20)
        >>> dq
        ─┬────┬────┬─
        ⟷│ 10 │ 20 │⟷
        ─┴────┴────┴─
        >>> dq.pop_right()
        20
        >>> dq
        ─┬────┬─
        ⟷│ 10 │⟷
        ─┴────┴─
        """
        return super().dequeue()

    def clear(self):
        """
        Removes all objects within the `Deque()` instance in constant time.

        Example
        -------
        >>> dq = Deque()
        >>> dq.append_right(1)
        >>> dq.append_left(2)
        >>> dq.append_right(3)
        >>> dq
        ─┬───┬───┬───┬─
        ⟷│ 2 │ 1 │ 3 │⟷
        ─┴───┴───┴───┴─
        >>> len(dq)
        3
        >>> dq.clear()
        >>> dq
        ─┬
        ⟷│
        ─┴
        >>> len(dq)
        0

        Note
        ----
        When you clear the `Deque()` instance, the `max_capacity` of the
        cleared instance remains the same as the one before.
        """
        super().clear()
