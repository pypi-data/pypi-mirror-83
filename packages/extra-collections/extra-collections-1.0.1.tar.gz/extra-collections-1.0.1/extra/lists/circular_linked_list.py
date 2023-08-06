"""
A circular linked list is a simple linear data structure where objects are
linked using pointers to their associated location. Unlike arrays whose objects
are stored at continuous locations. Each node stores a reference to an object
that is an element of the sequence, as well as a reference to the next node of
the circular linked list.

The first node of a circular linked list is known as the **head** of the linked
list. And the last node is known as the **tail**. The **tail** of a circular
linked list always points to the **head**.
"""
from extra.lists.linked_list import LinkedList


class CircularLinkedList(LinkedList):
    """
    A circular linked list is a simple linear data structure where objects are
    linked using pointers to their associated location. Unlike arrays whose
    objects are stored at continuous locations. Each node stores a reference to
    an object that is an element of the sequence, as well as a reference to the
    next node of the circular linked list.
    """

    __name__ = "extra.CircularLinkedList()"

    def __init__(self, iterable=None):
        """
        Initializes a `CircularLinkedList()` instance using an optional
        iterable in time-complexity of O(n) where **n** is the number of
        elements inside the given `iterable`.

        Parameters
        ----------
        iterable: iterable, optional
            An iterable python object that implements the `__iter__` method.
            For example, `list` and `tuple` are both iterables.

        Raises
        ------
        TypeError:
            It can be raised in two cases
                1. In case the given object isn't iterable.
                2. If one of the iterable elements is an `Extra` object.
        ValueError:
            If one of the iterable elements is `None`.

        Examples
        --------
        >>> cll = CircularLinkedList([10, -5, 7, 9])
        >>> cll
        ┌────┐ ┌────┐ ┌───┐ ┌───┐
        │ 10 │⟶│ -5 │⟶│ 7 │⟶│ 9 │⟶ ┐
        └────┘ └────┘ └───┘ └───┘  │
           ↑                       │
           └───────────────────────┘

        Using an iterable object with `None` as one of its elements will raise
        `ValueError`

        >>> CircularLinkedList([2, None])
        ValueError: Can't use `None` as an element within \
            `extra.CircularLinkedList()`!!

        Using a non-iterable object will raise `TypeError`

        >>> CircularLinkedList(2)
        TypeError: The given object isn't iterable!!

        Using nested `CircularLinkedList` objects will raise `TypeError` as
        well:

        >>> cll_1 = CircularLinkedList([1])
        >>> cll_2 = CircularLinkedList([1, cll_1])
        TypeError: Can't create `extra.CircularLinkedList()` using \
            `extra.CircularLinkedList()`!!

        Note
        -----
        Since most of the data structures found in this package are iterables,
        then you can use this classmethod to convert from one data structure to
        `CircularLinkedList` just like so:

        >>> ll = LinkedList([2, 5])
        >>> cll = CircularLinkedList(ll)
        >>> cll
        ┌───┐ ┌───┐
        │ 2 │⟶│ 5 │⟶ ┐
        └───┘ └───┘  │
          ↑          │
          └──────────┘
        """
        super().__init__(iterable)

    def _create_instance(self):
        """
        Returns an instance of the class.

        Returns
        -------
        CircularLinkedList():
            It returns an empty CircularLinkedList() instance.
        """
        return CircularLinkedList()

    # =============================     PRINT    ==============================
    def __repr__(self):
        """
        Represents the `CircularLinkedList()` instance as a string.

        Returns
        -------
        str:
            The string-representation of the `CircularLinkedList()` instance.

        Example
        -------
        >>> cll = CircularLinkedList([20, 77, 10, 6, 2])
        >>> cll
        ┌────┐ ┌────┐ ┌────┐ ┌───┐ ┌───┐
        │ 20 │⟶│ 77 │⟶│ 10 │⟶│ 6 │⟶│ 2 │⟶ ┐
        └────┘ └────┘ └────┘ └───┘ └───┘  │
           ↑                              │
           └──────────────────────────────┘
        """
        if super().is_empty():
            return super()._print_empty_linked_list()
        fst_line, sec_line, thrd_line = super()._print_linked_list(self._head)
        # backtrace representation
        sec_line += [" ┐"]
        thrd_line += [" │"]

        first_line = "".join(fst_line)
        second_line = "".join(sec_line)
        third_line = "".join(thrd_line)

        head_data = str(self._head.get_data())
        left_offset = (len(head_data) + 4) // 2
        remaining = (len(second_line) - 2) - left_offset

        fourth_line = (" " * left_offset) + "↑" + (" " * (remaining)) + "│"
        fifth_line = (" " * left_offset) + "└" + ("─" * (remaining)) + "┘"
        return "{}\n{}\n{}\n{}\n{}".format(
            first_line, second_line, third_line, fourth_line, fifth_line
        )

    # =============================    LENGTH    ==============================
    def __len__(self):
        """
        Gets the length of the `CircularLinkedList()` in constant time.

        Returns
        -------
        int:
            The length of the `CircularLinkedList()` instance. By Length, I
            mean the number of nodes of in the instance.

        Examples
        --------
        >>> cll = CircularLinkedList()
        >>> len(cll)
        0
        >>> cll = CircularLinkedList((2, 5, 0))
        >>> len(cll)
        3
        """
        return self._length

    def is_empty(self):
        """
        Checks if `CircularLinkedList()` instance is empty or not in constant
        time.

        Returns
        -------
        bool:
            A boolean flag showing if the CircularLinkedList() instance is
            empty or not. `True` shows that this instance is empty and `False`
            shows it's not empty.

        Example
        --------
        >>> cll = CircularLinkedList()
        >>> cll.is_empty()
        True
        >>> cll.add_front(5)
        >>> cll.is_empty()
        False
        """
        return self._length == 0

    # =============================   OPERATOR   ==============================
    def __iter__(self):
        """
        Iterates over the `CircularLinkedList()` instance and returns a
        generator in time-complexity of O(n) where **n** is the number of
        elements in the `CircularLinkedList()` instance.

        Yields
        ------
        generator:
            The value of each node in the instance.

        Examples
        --------
        >>> cll = CircularLinkedList([1, 2, 3])
        >>> for item in cll:
        ...     print(item)
        1
        2
        3
        """
        return super().__iter__()

    def __eq__(self, other):
        """
        Checks if two `CircularLinkedList()` instances are equal to each other.
        And this happens if, and only if, the following two conditions are met:

        1. The two instances are equal in length (same number of elements).

        2. Every single element in the first instance is equal, in both
        **value** and **type**, to the opposing element of the other instance.

        Parameters
        ----------
        other: CircularLinkedList()
            The other instance that we want to compare with the current one

        Returns
        -------
        bool:
            `True` if both instances are equal, and `False` otherwise.

        Raises
        ------
        TypeError:
            This happens in two cases
                1. If the other instance isn't an instance of
                `CircularLinkedList()`.
                2. In case one element in the first instance doesn't match the
                type of the opposing element in the other instance.

        Examples
        --------
        >>> cll_1 = CircularLinkedList([1, 2, 3])
        >>> cll_2 = CircularLinkedList([1, 3, 2])
        >>> cll_1 == cll_2
        False
        >>> cll_1 == cll_1
        True
        """
        return super().__eq__(other)

    def __ne__(self, other):
        """
        Checks if two `CircularLinkedList()` instances are NOT equal to each
        other. And this happens if, and only if, either one of the following
        two conditions is satisfied:

        1. The two instances are NOT equal in length (number of elements).

        2. Just one element in the first instance is NOT equal, in either
        **value** or **type**, to the opposing element of the other instance.

        Parameters
        ----------
        other: CircularLinkedList()
            The other instance that we want to compare with the current one

        Returns
        -------
        bool:
            `True` if both instances are NOT equal, and `False` otherwise.

        Raises
        ------
        TypeError:
            This happens in two cases
                1. If the other instance isn't an instance of
                `CircularLinkedList()`.
                2. In case one element in the first instance doesn't match the
                type of  the opposing element in the other instance.

        Examples
        --------
        >>> cll_1 = CircularLinkedList([1, 2, 3])
        >>> cll_2 = CircularLinkedList([1, 3, 2])
        >>> cll_1 != cll_2
        True
        >>> cll_1 != cll_1
        False
        """
        return super().__ne__(other)

    def __lt__(self, other):
        """
        Checks if the first `CircularLinkedList()` instance is less than the
        other instance. And this happens if all elements in the first instance
        are equal with at least one element less than the opposing element of
        the second instance.

        Parameters
        ----------
        other: CircularLinkedList()
            The other instance that we want to compare with the current one

        Returns
        -------
        bool:
            `True` if the first instance is less than the second, and `False`
            otherwise.

        Raises
        ------
        TypeError:
            This happens in two cases
                1. If the other instance isn't an instance of
                `CircularLinkedList()`.
                2. In case one element in the first instance doesn't match the
                type of the opposing element in the other instance.

        Examples
        --------
        >>> cll_1 = CircularLinkedList([1, 3, 2])
        >>> cll_2 = CircularLinkedList([1, 3, 3])
        >>> cll_1 < cll_2
        True

        >>> cll_1 = CircularLinkedList([1, 3])
        >>> cll_2 = CircularLinkedList([1, 3, 3])
        >>> cll_1 < cll_2
        True

        >>> cll_1 = CircularLinkedList([1, 5])
        >>> cll_2 = CircularLinkedList([1, 3, 3])
        >>> cll_1 < cll_2
        False

        >>> cll_1 = CircularLinkedList([5, 2, 1])
        >>> cll_2 = CircularLinkedList([1, 3, 3])
        >>> cll_1 < cll_2
        False

        >>> cll_1 = CircularLinkedList([1, 2, 3])
        >>> cll_2 = CircularLinkedList([1, 2, 3])
        >>> cll_1 < cll_2
        False
        """
        return super().__lt__(other)

    def __le__(self, other):
        """
        Checks if the first `CircularLinkedList()` instance is less than or
        equal to the other instance. And this happens if all elements in the
        first instance are equal or less than the opposing elements of the
        second instance.

        Parameters
        ----------
        other: CircularLinkedList()
            The other instance that we want to compare with the current one

        Returns
        -------
        bool:
            `True` if the first instance is less than or equal to the second
            instance, and `False` otherwise.

        Raises
        ------
        TypeError:
            This happens in two cases
                1. If the other instance isn't an instance of
                `CircularLinkedList()`.
                2. In case one element in the first instance doesn't match the
                type of the opposing element in the other instance.

        Examples
        --------
        >>> cll_1 = CircularLinkedList([1, 3, 2])
        >>> cll_2 = CircularLinkedList([1, 3, 3])
        >>> cll_1 <= cll_2
        True

        >>> cll_1 = CircularLinkedList([1, 3])
        >>> cll_2 = CircularLinkedList([1, 3, 3])
        >>> cll_1 <= cll_2
        True

        >>> cll_1 = CircularLinkedList([1, 5])
        >>> cll_2 = CircularLinkedList([1, 3, 3])
        >>> cll_1 <= cll_2
        False

        >>> cll_1 = CircularLinkedList([5, 2, 1])
        >>> cll_2 = CircularLinkedList([1, 3, 3])
        >>> cll_1 <= cll_2
        False

        >>> cll_1 = CircularLinkedList([1, 2, 3])
        >>> cll_2 = CircularLinkedList([1, 2, 3])
        >>> cll_1 <= cll_2
        True
        """
        return super().__le__(other)

    def __gt__(self, other):
        """
        Checks if the first `CircularLinkedList()` instance is greater than the
        other instance. And this happens if all elements in the first instance
        are equal with at least one element greater than the opposing element
        of the second instance.

        Parameters
        ----------
        other: CircularLinkedList()
            The other instance that we want to compare with the current one

        Returns
        -------
        bool:
            `True` if the first instance is greater than the second, and
            `False` otherwise.

        Raises
        ------
        TypeError:
            This happens in two cases
                1. If the other instance isn't an instance of
                `CircularLinkedList()`.
                2. In case one element in the first instance doesn't match the
                type of the opposing element in the other instance.

        Examples
        --------
        >>> cll_1 = CircularLinkedList([1, 3, 5])
        >>> cll_2 = CircularLinkedList([1, 3, 3])
        >>> cll_1 > cll_2
        True

        >>> cll_1 = CircularLinkedList([1, 3, 2, 1])
        >>> cll_2 = CircularLinkedList([1, 3, 2])
        >>> cll_1 > cll_2
        True

        >>> cll_1 = CircularLinkedList([1, 2])
        >>> cll_2 = CircularLinkedList([1, 3, 3])
        >>> cll_1 > cll_2
        False

        >>> cll_1 = CircularLinkedList([5, 2, 1])
        >>> cll_2 = CircularLinkedList([1, 3, 3])
        >>> cll_1 > cll_2
        False

        >>> cll_1 = CircularLinkedList([1, 2, 3])
        >>> cll_2 = CircularLinkedList([1, 2, 3])
        >>> cll_1 > cll_2
        False
        """
        return super().__gt__(other)

    def __ge__(self, other):
        """
        Checks if the first `CircularLinkedList()` instance is greater than or
        equal to the other instance. And this happens if all elements in the
        first instance are greater than or equal to the opposing element of the
        second instance.

        Parameters
        ----------
        other: CircularLinkedList()
            The other instance that we want to compare with the current one

        Returns
        -------
        bool:
            `True` if the first instance is greater than or equal to the
            second, and `False` otherwise.

        Raises
        ------
        TypeError:
            This happens in two cases
                1. If the other instance isn't an instance of
                `CircularLinkedList()`.
                2. In case one element in the first instance doesn't match the
                type of the opposing element in the other instance.

        Examples
        --------
        >>> cll_1 = CircularLinkedList([1, 3, 5])
        >>> cll_2 = CircularLinkedList([1, 3, 3])
        >>> cll_1 >= cll_2
        True

        >>> cll_1 = CircularLinkedList([1, 3, 2, 1])
        >>> cll_2 = CircularLinkedList([1, 3, 2])
        >>> cll_1 >= cll_2
        True

        >>> cll_1 = CircularLinkedList([1, 2])
        >>> cll_2 = CircularLinkedList([1, 3, 3])
        >>> cll_1 >= cll_2
        False

        >>> cll_1 = CircularLinkedList([5, 2, 1])
        >>> cll_2 = CircularLinkedList([1, 3, 3])
        >>> cll_1 >= cll_2
        False

        >>> cll_1 = CircularLinkedList([1, 2, 3])
        >>> cll_2 = CircularLinkedList([1, 2, 3])
        >>> cll_1 >= cll_2
        True
        """
        return super().__ge__(other)

    # =============================    SEARCH    ==============================
    def __contains__(self, value):
        """
        Checks if the given value exists in the `CircularLinkedList()` instance
        in time-complexity of O(n) where **n** is the total number of elements
        in the `CircularLinkedList()` instance.

        Parameters
        ----------
        value: Object
            The value to be searched for in the `CircularLinkedList()`
            instance.

        Returns
        -------
        bool:
            `True` if the given value exists in the `CircularLinkedList()`
            instance, and `False` otherwise.

        Examples
        --------
        >>> cll = CircularLinkedList([1, 3, 5])
        >>> 1 in cll
        True
        >>> 0 in cll
        False
        >>> "hello" in cll
        False
        """
        for item in self:
            if item == value:
                return True
        return False

    def _validate_index(self, idx, accept_negative=False, accept_slice=False):
        """
        Checks the validity of the given index. It raises the appropriate error
        when the index isn't valid and it returns nothing if the index is
        valid.

        Parameters
        ----------
        idx: int
            The index value.
        accept_negative: bool
            A flag to enable accepting negative indices, default `False`.
        accept_slice: bool
            A flag to enable accepting `slice` objects, default `False`.

        Raises
        ------
        TypeError:
            If the given index isn't `int`.
        IndexError:
            This happens in one of the following cases:
                1. if the given index is a `slice` object while `accept_slice`
                flag is `False`.
                2. If the given index is negative while `accept_negative` flag
                is `False`.

        Examples
        --------
        >>> cll = CircularLinkedList([1, 2, 3])
        >>> cll._validate_index('1')
        TypeError: Given index must be an integer!!
        >>> cll._validate_index(-2)
        IndexError: Negative indexing isn't supported with this functinoality!!
        >>> cll._validate_index(slice(0, 2))
        IndexError: Slice indexing isn't supported with this functinoality!!

        And it would return nothing if the given index if valid:

        >>> cll._validate_index(2)
        >>> cll._validate_index(-2, accept_negative=True)
        >>> cll._validate_index(slice(0, 2), accept_slice=True)
        """
        if isinstance(idx, slice):
            if not accept_slice:
                raise IndexError(
                    "Slice indexing isn't supported with this functinoality!!"
                )
        elif type(idx) != int:
            raise TypeError("Given index must be an integer!!")
        elif idx <= -1 and not accept_negative:
            raise IndexError(
                "Negative indexing isn't supported with this functinoality!!"
            )

    def __getitem__(self, idx):
        """
        Retrieves the element at the given index. The given index must be a
        zero-based `int`. This method doesn't support neither negative indexing
        nor `slice` objects. This method does that in time-complexity of O(k%n)
        where **k** is the given index and **n** is the number of elements
        found in the `CircularLinkedList()` instance.

        Parameters
        ----------
        idx: int
            The index to be used to retrieve value from `CircularLinkedList()`
            instance.

        Returns
        -------
        object:
            It returns the value stored at this the given index.

        Raises
        ------
        TypeError:
            If the given index isn't `int`.
        IndexError:
            If `CircularLinkedList()` instance is empty.

        Examples
        --------
        >>> cll = CircularLinkedList([1, 2, 3, 4, 5])
        >>> cll[0]
        1
        >>> cll[-2]
        4
        >>> cll[10]
        1

        Note
        ----
        Notice that the only case this method raises an `IndexError` is when
        the `CircularLinkedList()` instance is empty. Other than that, the
        method will keep iterating over the `CircularLinkedList()` instance
        till it reaches the given index. That's why even though the previous
        `CircularLinkedList()` instance is five-elements long, the method
        doesn't raise and `IndexError` when trying to retrieve the 10th
        element.
        """
        self._validate_index(idx)
        if self.is_empty():
            raise IndexError(f"{self.__name__} is empty!!")
        idx = idx % self._length if self._length != 0 else 0
        return super().__getitem__(idx)

    # =============================    INSERT    ==============================
    def _insert_node(self, prev_node, new_node):
        """
        Inserts a `new_node` at a position defined by the given `prev_node`.

        Parameters
        ----------
        prev_node: Node()
            A reference to the node next to which a new node should be inserted
        new_node: Node()
            A referece to the new node to be inserted.

        Returns
        -------
        Node():
            A reference to the new node after being inserted in the
            `CircularLinkedList()` instance.

        Raises
        ------
        AssertionError:
            This happens in one of the following cases:
                1. The `prev_node` isn't a `Node()` object or `None`.
                2. The `new_node` isn't a `Node()` object

        Example
        -------
        >>> cll = CircularLinkedList([1, 2, 3])
        >>> new_node = Node(10)
        >>> cll._insert_node(cll._head, new_node)
        Node(data: 10, next: 2)
        """
        assert prev_node is None or isinstance(prev_node, self._basic_node)
        assert isinstance(new_node, self._basic_node)

        # start inserting the node
        if self._length == 0:
            new_node.set_next(new_node)
            self._head = new_node
        elif prev_node is None:
            new_node.set_next(self._head.get_next())
            self._head.set_next(new_node)
            # swap data between new_node and self._head
            new_node._data, self._head._data = self._head._data, new_node._data
            new_node = self._head  # to be returned
        else:
            new_node.set_next(prev_node.get_next())
            prev_node.set_next(new_node)
        self._length += 1
        return new_node

    def add_front(self, item):
        """
        Adds the given value at the head of the `CircularLinkedList()` instance
        in constant time.

        Parameters
        ----------
        item: object
            The value to be inserted at the `CircularLinkedList()` head.

        Raises
        ------
        TypeError:
            If the given item is an instance of `Extra`.
        ValueError:
            If the given item is `None`.

        Examples
        --------
        >>> cll = CircularLinkedList([1, 2, 3])
        >>> cll.add_front(10)
        >>> cll
        ┌────┐ ┌───┐ ┌───┐ ┌───┐
        │ 10 │⟶│ 1 │⟶│ 2 │⟶│ 3 │⟶ ┐
        └────┘ └───┘ └───┘ └───┘  │
           ↑                      │
           └──────────────────────┘
        """
        super().add_front(item)

    def add_end(self, item):
        """
        Adds the given value at the tail of the `CircularLinkedList()` instance
        in time-complexity of O(n) where **n** is the number of elements in the
        instance.

        Parameters
        ----------
        item: object
            The value to be inserted at the `CircularLinkedList()` tail.

        Raises
        ------
        TypeError:
            If the given item is an instance of `Extra`.
        ValueError:
            If the given item is `None`.

        Examples
        --------
        >>> cll = CircularLinkedList([1, 2, 3])
        >>> cll.add_end(10)
        >>> cll
        ┌───┐ ┌───┐ ┌───┐ ┌────┐
        │ 1 │⟶│ 2 │⟶│ 3 │⟶│ 10 │⟶ ┐
        └───┘ └───┘ └───┘ └────┘  │
          ↑                       │
          └───────────────────────┘
        """
        super().add_end(item)

    def insert(self, idx, item):
        """
        Insertd a value to the `CircularLinkedList()` instance at a position
        defined by the given index.

        Parameters
        ----------
        idx: int
            An integer pointing to the index at which the given value should be
            inserted.
        item: object
            An object to be inserted.

        Raises
        ------
        IndexError:
            This happens only if the index is less than zero (-ve).
        TypeError:
            This happens in one of the following cases:
                1. If the given index isn't integer.
                2. If the given item is an instance of `Extra`.
        ValueError:
            If the given item is `None`.

        Example
        -------
        >>> cll = CircularLinkedList([1, 2, 3])
        >>> cll.insert(1, item=10)
        >>> cll
        ┌───┐ ┌────┐ ┌───┐ ┌───┐
        │ 1 │⟶│ 10 │⟶│ 2 │⟶│ 3 │⟶ ┐
        └───┘ └────┘ └───┘ └───┘  │
          ↑                       │
          └───────────────────────┘
        >>> cll.insert(15, item=8)  #index is bigger than instance length
        >>> cll
        ┌───┐ ┌───┐ ┌────┐ ┌───┐ ┌───┐
        │ 8 │⟶│ 1 │⟶│ 10 │⟶│ 2 │⟶│ 3 │⟶ ┐
        └───┘ └───┘ └────┘ └───┘ └───┘  │
          ↑                             │
          └─────────────────────────────┘
        >>> cll.insert(1, item=None)
        >>> cll
        ValueError: Can't use `None` as an element within \
            `extra.CircularLinkedList()`!!
        >>> cll.insert(-1, item=100)
        >>> cll
        IndexError: Negative indexing isn't supported with this functinoality!!
        """
        self._validate_index((idx))
        self._validate_item(item)
        idx = idx % (self._length + 1)
        super()._insert(idx, item)

    def extend(self, other):
        """
        Extends the current `CircularLinkedList()` instance by appending the
        elements of the other `CircularLinkedList()` instance in time-
        complexity of O(n+m) where **n** is the number of elements in the
        original instance and **m** is the number of elements in the other
        instance.

        Parameters
        ----------
        other: CircularLinkedList()
            The `CircularLinkedList()` instance whose elements will be appended

        Raises
        ------
        TypeError:
            If the given object isn't a `CircularLinkedList()` instance.

        Example
        -------
        >>> cll_1 = CircularLinkedList([1, 2])
        >>> cll_1
        ┌───┐ ┌───┐
        │ 1 │⟶│ 2 │⟶ ┐
        └───┘ └───┘  │
          ↑          │
          └──────────┘
        >>> cll_2 = CircularLinkedList([3, 4, 5])
        >>> cll_1.extend(cll_2)
        >>> cll_1
        ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐
        │ 1 │⟶│ 2 │⟶│ 3 │⟶│ 4 │⟶│ 5 │⟶ ┐
        └───┘ └───┘ └───┘ └───┘ └───┘  │
          ↑                            │
          └────────────────────────────┘
        >>> cll_1.extend([6, 7])
        TypeError: Type Mismatch! Can't extend `extra.CircularLinkedList()` \
            with `<class 'list'>`!!
        """
        if not isinstance(other, self.__class__):
            raise TypeError(
                "Type Mismatch! "
                + f"Can't extend `{self.__name__}` with `{type(other)}`!!"
            )
        if not other.is_empty():
            counter = 0
            curr_node = self._head if not self.is_empty() else None
            while counter < self._length - 1:
                counter += 1
                curr_node = curr_node.get_next()
            prev_node = curr_node
            # now, let's add the new values
            for item in other:
                new_node = self._basic_node(item)
                self._insert_node(prev_node, new_node)
                prev_node = new_node

    # =============================      SET     ==============================
    def __setitem__(self, idx, item):
        """
        Replaces the value at the given index with the given item. It does that
        in time-complexity of O(k%n) where **k** is the index value and **n**
        is the number of elements in the `CircularLinkedList()` instance.

        Parameters
        ----------
        idx: int
            An integer pointing to the index at which the given value should be
            inserted.
        item: object
            An object to be inserted.

        Raises
        ------
        IndexError:
            If the given index is either negative or out of the boundaries.
        ValueError:
            If the given object is `None`.
        TypeError:
            This get raised in one of the following cases:
                1. If the given index type is not `int`.
                2. If the given object is an instance of `Extra`.

        TODO
        ----
        1. Handle negative indexing
        2. Handle slice objects

        Examples
        --------
        >>> cll = CircularLinkedList([1, 2, 3])
        >>> cll[0] = 10
        >>> cll[2] = 30
        >>> cll
        ┌────┐ ┌───┐ ┌────┐
        │ 10 │⟶│ 2 │⟶│ 30 │⟶ ┐
        └────┘ └───┘ └────┘  │
           ↑                 │
           └─────────────────┘
        >>> cll[-1] = 0
        IndexError: Negative indexing isn't supported with this functinoality!!
        >>> cll[31] = 20 #index is bigger than the instance length
        >>> cll
        ┌────┐ ┌────┐ ┌────┐
        │ 10 │⟶│ 20 │⟶│ 30 │⟶ ┐
        └────┘ └────┘ └────┘  │
           ↑                  │
           └──────────────────┘
        """
        self._validate_index(idx)
        idx = idx % self._length if self._length != 0 else 0
        super()._replace_value(idx, item)

    # =============================    REMOVE    ==============================
    def _remove_node(self, prev_node, node_to_be_removed):
        """
        Removes a node from the `CircularLinkedList()` instance defined by the
        `prev_node` object.

        Parameters
        ----------
        prev_node: Node()
            A reference to the node next to the node that will be removed.
        node_to_be_removed: Node()
            A referece to the node to be removed.

        Raises
        ------
        AssertionError:
            This happens in one of the following cases:
                1. The `prev_node` isn't a `Node()` object or `None.
                2. The `node_to_be_removed` isn't a `Node()` object

        Example
        -------
        >>> cll = CircularLinkedList([1, 2, 3])
        >>> cll
        ┌───┐ ┌───┐ ┌───┐
        │ 1 │⟶│ 2 │⟶│ 3 │⟶ ┐
        └───┘ └───┘ └───┘  │
          ↑                │
          └────────────────┘
        >>> cll._remove_node(cll._head, cll._head._next)
        >>> cll
        ┌───┐ ┌───┐
        │ 1 │⟶│ 3 │⟶ ┐
        └───┘ └───┘  │
          ↑          │
          └──────────┘
        """
        assert prev_node is None or isinstance(prev_node, self._basic_node)
        assert isinstance(node_to_be_removed, self._basic_node)

        # if node to be removed is the first
        if prev_node is None:
            if self._length == 1:
                self._head._data = None  # NOTE: don't use set_data() here
            else:
                next_to_head = self._head.get_next()
                self._head.set_data(next_to_head.get_data())
                self._head.set_next(next_to_head.get_next())
        else:
            prev_node.set_next(node_to_be_removed.get_next())
        self._length -= 1

    def __delitem__(self, idx):
        """
        Deletes the value at the given index. It does that in time-complexity
        of O(k%n) where **k** is the index value and **n** is the number of
        elements in the `CircularLinkedList()` instance.

        Parameters
        ----------
        idx: int
            An integer pointing to the index where the node that should be
            removed.

        Raises
        ------
        IndexError:
            If the given index is either negative or out of the boundaries.

        TODO
        ----
        1. Handle negative indexing
        2. Handle slice objects

        Examples
        --------
        >>> cll = CircularLinkedList([1, 2, 3])
        >>> del cll[0]
        >>> cll
        ┌───┐ ┌───┐
        │ 2 │⟶│ 3 │⟶ ┐
        └───┘ └───┘  │
          ↑          │
          └──────────┘
        >>> del cll[-1]
        IndexError: Negative indexing isn't supported with this functinoality!!
        >>> del cll[31]  #index is bigger than the instance length
        >>> cll
        ┌───┐
        │ 2 │⟶ ┐
        └───┘  │
          ↑    │
          └────┘
        """
        self._validate_index(idx)
        if not self.is_empty():
            idx = idx % self._length if self._length != 0 else 0
            super()._remove_idx(idx)

    def remove_front(self):
        """
        Removes the value at the head of the `CircularLinkedList()` instance in
        constant time.

        Examples
        --------
        >>> cll = CircularLinkedList([1, 2, 3])
        >>> cll.remove_front()
        >>> cll
        ┌───┐ ┌───┐
        │ 2 │⟶│ 3 │⟶ ┐
        └───┘ └───┘  │
          ↑          │
          └──────────┘
        >>> cll.remove_front()
        >>> cll
        ┌───┐
        │ 3 │⟶ ┐
        └───┘  │
          ↑    │
          └────┘
        """
        super().remove_front()

    def remove_end(self):
        """
        Removes the value at the tail of the `CircularLinkedList()` instance in
        time-complexity of O(k%n) where **k** is the index value and **n** is
        the number of elements in the `CircularLinkedList()` instance.

        Examples
        --------
        >>> cll = CircularLinkedList([1, 2, 3])
        >>> cll.remove_end()
        >>> cll
        ┌───┐ ┌───┐
        │ 1 │⟶│ 2 │⟶ ┐
        └───┘ └───┘  │
          ↑          │
          └──────────┘
        >>> cll.remove_end()
        >>> cll
        ┌───┐
        │ 1 │⟶ ┐
        └───┘  │
          ↑    │
          └────┘
        """
        super().remove_end()

    def remove(self, value, all=True):
        """
        Removes a single node or multiple nodes (in case of `all` being `True`)
        whose value equal to the given value from the `CircuarLinkedList()`
        instance.

        Parameters
        ----------
        value: object
            The value to be removed from the `CircularLinkedList()` instance.
        all: bool
            A flag (default: `True`); if `True`, all occurrences of the given
            value are remove. If `False`, only the first occurrence is removed.

        Raises
        ------
        ValueError:
            If The given value is `None`.
        TypeError:
            This get raised in one of the following cases:
                1. If the type of the `all` flag isn't boolean.
                2. If the given value is an instance of `Extra` class.

        Example
        -------
        >>> cll = CircularLinkedList([1, 2, 3, 2, 2])
        >>> cll
        ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐
        │ 1 │⟶│ 2 │⟶│ 3 │⟶│ 2 │⟶│ 2 │⟶ ┐
        └───┘ └───┘ └───┘ └───┘ └───┘  │
          ↑                            │
          └────────────────────────────┘
        >>> cll.remove(2, all=False)
        >>> cll
        ┌───┐ ┌───┐ ┌───┐ ┌───┐
        │ 1 │⟶│ 3 │⟶│ 2 │⟶│ 2 │⟶ ┐
        └───┘ └───┘ └───┘ └───┘  │
          ↑                      │
          └──────────────────────┘
        >>> cll.remove(10) #does nothing
        >>> cll.remove(2)
        >>> cll
        ┌───┐ ┌───┐
        │ 1 │⟶│ 3 │⟶ ┐
        └───┘ └───┘  │
          ↑          │
          └──────────┘
        """
        super().remove(value, all)

    def clear(self):
        """
        Removes all nodes within the `CircularLinkedList()` in constant time.

        Example
        -------
        >>> cll = CircularLinkedList([1, 2, 3])
        >>> cll
        ┌───┐ ┌───┐ ┌───┐
        │ 1 │⟶│ 2 │⟶│ 3 │⟶ ┐
        └───┘ └───┘ └───┘  │
          ↑                │
          └────────────────┘
        >>> cll.clear()
        >>> cll.is_empty()
        True
        >>> cll
        ┌─
        │
        └─
        """
        super().clear()

    # =============================     SPLIT    ==============================
    def split(self, idx):
        """
        Splits the `CircularLinkedList()` instance into two instances based on
        the given index in time-complexity of O(min(k,n/2)) where **k** is the
        index and **n** is the number of elements in the original instance. We
        can consider `idx` as the start index of the second
        `CircularLinkedList()` after splitting. If `idx=0`, the first returned
        `CircularLinkedList()` will be empty while the second returned
        `CircularLinkedList()` will be the same length as the original.

        Parameters
        ----------
        idx: int
            A positive integer pointing to the index at which the
            `CircularLinkedList()` instance should be split.

        Returns
        -------
        CircularLinkedList():
            The left CircularLinkedList() instance returned after split.
        CircularLinkedList():
            The right CircularLinkedList() instance returned after split

        Raises
        ------
        TypeError:
            If the given index isn't `int`.
        IndexError:
            If the given index is either negative or out of the
            `CircularLinkedList()` boundaries.

        Examples
        --------
        >>> cll = CircularLinkedList([1, 2, 3])
        >>> cll
        ┌───┐ ┌───┐ ┌───┐
        │ 1 │⟶│ 2 │⟶│ 3 │⟶ ┐
        └───┘ └───┘ └───┘  │
          ↑                │
          └────────────────┘
        >>> left, right = cll.split(1)
        >>> left
        ┌───┐
        │ 1 │⟶ ┐
        └───┘  │
          ↑    │
          └────┘
        >>> right
        ┌───┐ ┌───┐
        │ 2 │⟶│ 3 │⟶ ┐
        └───┘ └───┘  │
          ↑          │
          └──────────┘
        """
        self._validate_index(idx)
        idx = idx % self._length if self._length != 0 else 0
        return super()._split(idx)

    # =============================   ROTATION   ==============================
    def rotate_left(self, distance, inplace=True):
        """
        Rotates the `CircularLinkedList()` instance to the left by a number of
        times defined by the `distance`. If `inplace=True`, it does the
        rotation in-place. If not, it returns the rotated instance. The
        time-compelxity of this method is of O(k%n) where **k** is the index
        and **n** is the number of elements in the `CircularLinkedList()`
        instance.

        Parameters
        ----------
        distance: int
            The rotation distance to the left.
        inplace: bool
            A flag to determine if the rotation is going to be in-place or not.
            (default `True`).

        Returns
        -------
        CircularLinkedList():
            The rotated instance if `inplace=True`

        Examples
        --------
        >>> cll = CircularLinkedList([1, 2, 3, 4])
        >>> cll
        ┌───┐ ┌───┐ ┌───┐ ┌───┐
        │ 1 │⟶│ 2 │⟶│ 3 │⟶│ 4 │⟶ ┐
        └───┘ └───┘ └───┘ └───┘  │
          ↑                      │
          └──────────────────────┘
        >>> cll.rotate_left(1)
        >>> cll
        ┌───┐ ┌───┐ ┌───┐ ┌───┐
        │ 2 │⟶│ 3 │⟶│ 4 │⟶│ 1 │⟶ ┐
        └───┘ └───┘ └───┘ └───┘  │
          ↑                      │
          └──────────────────────┘
        >>> # it works just fine when the distance is bigger than the
        >>> # length of the circular linked list instance
        >>> cll.rotate_left(10)
        >>> cll
        ┌───┐ ┌───┐ ┌───┐ ┌───┐
        │ 4 │⟶│ 1 │⟶│ 2 │⟶│ 3 │⟶ ┐
        └───┘ └───┘ └───┘ └───┘  │
          ↑                      │
          └──────────────────────┘
        """
        return super().rotate_left(distance, inplace)

    def rotate_right(self, distance, inplace=True):
        """
        Rotates the `CircularLinkedList()` instance to the right by a number of
        times defined by the given `distance`. If `inplace=True`, it does the
        rotation in-place. If not, it returns the rotated instance. The time-
        compelxity of this method is O(k%n) where **k** is the index and **n**
        is the number of elements in the `CircularLinkedList()` instance.

        Parameters
        ----------
        distance: int
            The rotation distance to the right.
        inplace: bool
            A flag to determine if the rotation is going to be in-place or not.
            (default `True`).

        Returns
        -------
        CircularLinkedList():
            The rotated instance if `inplace=True`

        Examples
        --------
        >>> cll = CircularLinkedList([1, 2, 3, 4])
        >>> cll
        ┌───┐ ┌───┐ ┌───┐ ┌───┐
        │ 1 │⟶│ 2 │⟶│ 3 │⟶│ 4 │⟶ ┐
        └───┘ └───┘ └───┘ └───┘  │
          ↑                      │
          └──────────────────────┘
        >>> cll.rotate_right(1)
        >>> cll
        ┌───┐ ┌───┐ ┌───┐ ┌───┐
        │ 4 │⟶│ 1 │⟶│ 2 │⟶│ 3 │⟶ ┐
        └───┘ └───┘ └───┘ └───┘  │
          ↑                      │
          └──────────────────────┘
        >>> # it works just fine when the distance is bigger than the
        >>> # length of the circular linked list instance
        >>> cll.rotate_right(14)
        >>> cll
        ┌───┐ ┌───┐ ┌───┐ ┌───┐
        │ 2 │⟶│ 3 │⟶│ 4 │⟶│ 1 │⟶ ┐
        └───┘ └───┘ └───┘ └───┘  │
          ↑                      │
          └──────────────────────┘
        """
        return super().rotate_right(distance, inplace)

    # =============================     MISC     ==============================
    def reverse(self):
        """
        Reverses the whole `CircularLinkedList()` instance in time-complexity
        of O(n) where **n** is the number of elements in the instance.

        Returns
        -------
        CircularLinkedList():
            The reversed CircularLinkedList() instance.

        Example
        -------
        >>> cll = CircularLinkedList([1, 2, 3, 4])
        >>> cll
        ┌───┐ ┌───┐ ┌───┐ ┌───┐
        │ 1 │⟶│ 2 │⟶│ 3 │⟶│ 4 │⟶ ┐
        └───┘ └───┘ └───┘ └───┘  │
          ↑                      │
          └──────────────────────┘
        >>> cll.reverse()
        ┌───┐ ┌───┐ ┌───┐ ┌───┐
        │ 4 │⟶│ 3 │⟶│ 2 │⟶│ 1 │⟶ ┐
        └───┘ └───┘ └───┘ └───┘  │
          ↑                      │
          └──────────────────────┘
        """
        return super().reverse()

    def to_list(self):
        """
        Converts the `CircularLinkedList()` instance to a `list` in time-
        complexity of O(n) where **n** is the number of elements in the
        `CircularLinkedList()` instance.

        Returns
        -------
        list:
            A `list` object containing the same elements as the
            `CircularLinkedList()` instance.

        Example
        -------
        >>> cll = CircularLinkedList()
        >>> cll.add_front(20)
        >>> cll.add_front(10)
        >>> cll.add_end(30)
        >>> cll
        ┌────┐ ┌────┐ ┌────┐
        │ 10 │⟶│ 20 │⟶│ 30 │⟶ ┐
        └────┘ └────┘ └────┘  │
           ↑                  │
           └──────────────────┘
        >>> cll.to_list()
        [10, 20, 30]
        """
        return super().to_list()

    def count(self, value):
        """
        Counts the number of occurrence the given value is in the
        `CircularLinkedList()` instance.

        Parameters
        ----------
        value: object
            The object to count its occurrences

        Returns
        -------
        int:
            The number of times the given value is found in the
            `CircularLinkedList()` instance. And 0 if it wasn't found.

        Example
        -------
        >>> cll = CircularLinkedList([0, 1, 1, 2, 3, 5])
        >>> cll.count(3)
        1
        >>> cll.count(1)
        2
        >>> cll.count("he")
        0
        """
        return super().count(value)

    def copy(self):
        """
        Copies the ``CircularLinkedList()`` instance in a shallow-manner.

        Returns
        -------
        CircularLinkedList():
            The shallow copy of the original instance.

        Example
        ------
        >>> cll = CircularLinkedList()
        >>> cll.add_end(10)
        >>> cll.add_end(20)
        >>> cll
        ┌────┐ ┌────┐
        │ 10 │⟶│ 20 │⟶ ┐
        └────┘ └────┘  │
           ↑           │
           └───────────┘
        >>> cll.copy()
        ┌────┐ ┌────┐
        │ 10 │⟶│ 20 │⟶ ┐
        └────┘ └────┘  │
           ↑           │
           └───────────┘
        """
        return super().copy()
