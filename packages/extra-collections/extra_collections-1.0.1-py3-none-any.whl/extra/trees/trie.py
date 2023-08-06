"""
A trie, pronounced "try", is a tree-based data structure for storing strings in
order to support fast pattern matching. Indeed, the name "trie" comes from the
word "retrieval". The primary query operations that tries support is "prefix
matching" which involves being given a string and looking for all the sequences
that contain the given string as a prefix.
"""
import warnings
from extra.trees.tree import TreeNode, Tree


class TrieNode(TreeNode):
    """
    A trie node is the basic unit for building tries. A tree node must contain
    a value and this value has to be a `str`. Each trie node has zero or more
    trie nodes as children.
    """

    __name__ = "extra.TrieNode()"

    def __init__(self, value):
        """
        Creates a `TrieNode()` object which is the basic unit for building
        Trie() objects!!

        Parameters
        ----------
        value: str
            The value to be saved within the `TrieNode()` instance

        Raises
        ------
        TypeError:
            If the given item is not a `str` object.
        """
        if type(value) != str:
            raise TypeError("Trienodes accept characters only!!")

        self._parent = None
        self._data = value
        self._children = {}
        self._is_word = False

    def get_characters(self):
        """
        Returns a list of all the character children following the current
        `TrieNode()` instance.

        Returns
        -------
        list:
            A list of all the characters obtained by the children.
        """
        return self._children.keys()

    def get_children(self):
        """
        Returns a list of all the children nodes of the current `TrieNode()`
        instance.

        Returns
        -------
        list:
            A list of all the children nodes of the current `TrieNode()`.
        """
        return list(self._children.values())

    def get_child(self, ch):
        """
        Gets the child that has the given character (`ch`) as a key.

        Parameters
        ----------
        ch: str
            A character that represents the child's key.

        Returns
        -------
        TrieNode() or None:
            If the key belongs to a certain `TrieNode()` child, this child is
            returned. If the key wasn't found, `None` is returned.
        """
        try:
            return self._children[ch]
        except KeyError:
            return None

    def get_parent(self):
        """
        Returns the parent of the current `TrieNode()` instance.

        Returns
        -------
        TrieNode() or None:
            A reference to the parent of the current `TrieNode()` which could
            be a `TrieNode() object or `None` in case the current `TrieNode()`
            is the root of the `Trie()` instance.
        """
        return self._parent

    def set_child(self, ch, new_node):
        """
        Sets the given `new_node` as a child for the current `TrieNode()` using
        the given `ch` as a new key.

        Parameters
        ----------
        ch: str
            The character that will be used as a key for the new node.

        new_node: TrieNode()
            The `TrieNode()` that will be a child for the current one.

        Raises
        ------
        TypeError:
            This can be raised due to the following reasons:
                1. The given key is not a `str`.
                2. If the given item is not an `TrieNode()` object.
        """
        if type(ch) != str:
            raise TypeError(
                f"Given key is `{type(ch)}` and it should be a `str`!!"
            )
        elif not isinstance(new_node, TrieNode):
            raise TypeError(
                f"You can't set a child unless it's an `{self.__name__}` "
                + "object!!"
            )
        self._children[ch] = new_node
        new_node._parent = self

    def is_leaf(self):
        """
        Checks if the current `TrieNode()` instance is a leaf node. A leaf node
        is a tree node that has no children.

        Returns
        -------
        bool:
            `True` if the current `TrieNode()` has no children and `False`
            otherwise.
        """
        return self._children == {}

    def __repr__(self):
        """
        Represents `TrieNode()` object as a string.

        Returns
        -------
        str:
            A string representing the `TrieNode()` instance.

        Example
        -------
        >>> x = TrieNode("x")
        >>> x
        TrieNode("x")
        """
        return f"TrieNode({self._data})"

    def _represent(self):
        """
        A helpful function used to represent the `TrieNode()` instance when
        printing. It's used with Tree.__repr__() method

        Note
        ----
        The following character: '✓' is appended to a the `TrieNode()` object
        if it's the last child in representing a whole word.
        """
        if self._is_word:
            return self._data + " ✓"
        else:
            return self._data


class Trie(Tree):
    """
    A trie is a tree-based data structure that can be defined recursively using
    a collection of tree nodes, where each node contains a string  value and
    each node has a list of references to the children tree nodes in a tree-
    form structure.
    """

    __name__ = "extra.Trie()"

    def __init__(self):
        """
        Creates an empty `Trie()` object!!

        Example
        -------
        >>> t = Trie()
        >>> type(t)
        <class 'extra.trees.trie.Trie'>
        >>> t
        --
        """
        self._root = TrieNode("ROOT")
        self._nodes_count = 1

    def _validate_item(self, word, accept_empty_string=True):
        """
        Makes sure the input variable type can be processed. The main use for
        this method is to make sure we can't create nested objects from the
        package.

        Parameters
        ----------
        word: str
            The input word as a string.
        accept_empty_string: bool
            A boolean to enable accepting empty strings as a valid input.
            `True` to consider an empty string as a valid input and `False` to
            consider it invalid.

        Raises
        -------
        ValueError:
            If the given `word` is empty and `accept_empty_string` is `False`.
        TypeError:
            If the type of the given `word` is not `str`.
        """
        super()._validate_item(word)
        if type(word) != str:
            raise TypeError(
                f"Can't deal with {type(word)} object since "
                + f"`{self.__name__}` contains only characters!!"
            )
        if not accept_empty_string and len(word.strip()) == 0:
            raise ValueError(
                f"White-spaces can't be used with `{self.__name__}`!!"
            )

    # =============================    LENGTH    ==============================
    def __len__(self):
        """
        Gets the length of the `Trie()` instance. Length is the number of nodes
        in the instance.


        Returns
        -------
        int:
            The length of the `Trie()` instance. Length is the number of nodes
            in the instance.

        Examples
        --------
        >>> t = Trie()
        >>> len(t)
        1
        >>> t.insert("car")
        >>> t.insert("cart")
        >>> t.insert("cast")
        >>> t
        ROOT
        └─┬ c
          └─┬ a
            ├─┬ r ✓
            │ └── t ✓
            └─┬ s
              └── t ✓
        >>> len(t)
        7
        """
        return self._nodes_count

    def is_empty(self):
        """
        Checks if the `Trie()` instance is empty or not in constant time.

        Returns
        -------
        bool:
            A boolean flag showing if the `Trie()` instance is empty or not.
            `True` shows that this instance is empty and `False` shows it's
            not empty.

        Example
        --------
        >>> t = Trie()
        >>> t.is_empty()
        True
        >>> t.insert("apple")
        >>> t.is_empty()
        False
        """
        return self._nodes_count == 1

    # =============================     PRINT    ==============================
    def __repr__(self):
        """
        Represents the `Trie()` instance as a string.

        Returns
        -------
        str:
            The string-representation of the `Trie()` instance.

        Example
        -------
        >>> t = Trie()
        >>> t
        --
        >>> t.insert("car")
        >>> t.insert("cart")
        >>> t.insert("cast")
        >>> t
        ROOT
        └─┬ c
          └─┬ a
            ├─┬ r ✓
            │ └── t ✓
            └─┬ s
              └── t ✓
        """
        return super().__repr__()

    # ============================= HEIGHT/DEPTH ==============================
    def get_height(self):
        """
        Gets the height of the `Trie()` instance. The trie's height is the
        number of edges between the root and the furthest leaf node.

        Returns
        -------
        int:
            A positive integer representing the height of the instance.

        Example
        -------
        >>> t = Trie()
        >>> t.insert("car")
        >>> t.insert("cart")
        >>> t.insert("cast")
        >>> t
        ROOT
        └─┬ c
          └─┬ a
            ├─┬ r ✓
            │ └── t ✓
            └─┬ s
              └── t ✓
        >>> t.get_height()
        4
        """
        return super().get_height()

    def get_depth(self):
        """
        Gets the depth of the `Trie()` instance.

        Returns
        -------
        int:
            A positive integer representing the depth of the given `Trie()`.

        Example
        -------
        >>> t = Trie()
        >>> t.insert("car")
        >>> t.insert("cart")
        >>> t.insert("cast")
        >>> t
        ROOT
        └─┬ c
          └─┬ a
            ├─┬ r ✓
            │ └── t ✓
            └─┬ s
              └── t ✓
        >>> t.get_depth()
        0
        """
        if self.is_empty():
            return 0
        return self._get_depth(self._root)

    # =============================  LEAF NODES  ==============================
    def count_leaf_nodes(self):
        """
        Counts the number of leaf nodes in the `Trie()` instance. Leaf nodes
        are the trie nodes that have no children.

        Returns
        -------
        int:
            A positive integer representing the number of leaf nodes in the
            `Trie()`.

        Example
        -------
        >>> t = Trie()
        >>> t.insert("car")
        >>> t.insert("cart")
        >>> t.insert("cast")
        >>> t
        ROOT
        └─┬ c
          └─┬ a
            ├─┬ r ✓
            │ └── t ✓
            └─┬ s
              └── t ✓
        >>> t.count_leaf_nodes()
        2
        """
        if self.is_empty():
            return 0
        return self._count_leaf_nodes(self._root)

    # =============================     ITER     ==============================
    def __iter__(self):
        """
        Iterates over the `Trie()` instance and returns a generator of the
        nodes values in breadth-first manner.

        Yields
        ------
        str:
            The string stored at each node in the instance.

        Example
        -------
        >>> t = Trie()
        >>> t.insert("car")
        >>> t.insert("cart")
        >>> t.insert("cast")
        >>> t
        ROOT
        └─┬ c
          └─┬ a
            ├─┬ r ✓
            │ └── t ✓
            └─┬ s
              └── t ✓
        >>> for value in t:
        ...     print(value, end=',')
        c,a,r,s,t,t,
        """
        if not self.is_empty():
            current_nodes = self._root.get_children()
            while len(current_nodes) > 0:
                next_nodes = []
                for node in current_nodes:
                    yield node.get_data()
                    next_nodes.extend(node.get_children())
                current_nodes = next_nodes

    def to_list(self):
        """
        Converts the `Trie()` instance to a `list` where values will be
        inserted in breadth-first manner.

        Returns
        -------
        list:
            A `list` object containing the same elements as the `Trie()`
            instance.

        Example
        -------
        >>> t = Trie()
        >>> t.insert("car")
        >>> t.insert("cart")
        >>> t.insert("cast")
        >>> t
        ROOT
        └─┬ c
          └─┬ a
            ├─┬ r ✓
            │ └── t ✓
            └─┬ s
              └── t ✓
        >>> t.to_list()
        ['c', 'a', 'r', 's', 't', 't']
        """
        return super().to_list()

    # =============================     FIND     ==============================
    def _follow_path(self, word):
        """
        Parses the `Trie()` instance and returns the last accessed node along
        side with the part of the word that can't be parsed.

        Parameters
        ----------
        word: str
            The string to search for inside the `Trie()` instance.

        Returns
        -------
        TrieNode():
            A reference to the last accessed node in the `Trie()` instance.
        str:
            The part of the given `word` that wasn't found in the `Trie()`
            instance.

        Raises
        ------
        AssertionError:
            If the given word isn't a `str`.

        Example
        -------
        >>> t = Trie()
        >>> t.insert("car")
        >>> t.insert("cart")
        >>> t.insert("cast")
        >>> t
        ROOT
        └─┬ c
          └─┬ a
            ├─┬ r ✓
            │ └── t ✓
            └─┬ s
              └── t ✓
        >>> node, remaining = t._follow_path("case")
        >>> node
        TrieNode(s)
        >>> remaining
        'e'
        """
        assert type(word) == str

        curr_node = self._root
        while word:
            ch = word[0]
            child = curr_node.get_child(ch)
            child_data = child.get_data() if child else "}"
            # '}' is used to break the following if-condition
            if child_data == word[: len(child_data)]:
                word = word[len(child_data):]
                curr_node = child
            else:
                break
        return curr_node, word

    def __contains__(self, word):
        """
        Searches the `Trie()` for the given `word` and returns `True` if the
        whole word exists and `False` if not.

        Parameters
        ----------
        word: str
            The word to be searched for in the `Trie()` instance.

        Returns
        -------
        bool:
            Returns `True` if the value exists in the `Trie()` instance and
            `False` if not.

        Example
        -------
        >>> t = Trie()
        >>> t.insert("car")
        >>> t.insert("cart")
        >>> t.insert("cast")
        >>> t
        ROOT
        └─┬ c
          └─┬ a
            ├─┬ r ✓
            │ └── t ✓
            └─┬ s
              └── t ✓
        >>> "car" in t
        True
        >>> "cas" in t
        False
        >>> "care" in t
        False
        """
        if type(word) != str:
            return False
        last_node, remaining_word = self._follow_path(word)
        return remaining_word == "" and last_node._is_word

    def has_prefix(self, prefix):
        """
        Searches the `Trie()` for the given `prefix` and returns `True` if the
        whole prefix exists and `False` if not.

        Parameters
        ----------
        prefix: str
            The prefix to be searched for in the `Trie()` instance.

        Returns
        -------
        bool:
            Returns `True` if the prefix exists in the `Trie()` instance and
            `False` if not.

        Example
        -------
        >>> t = Trie()
        >>> t.insert("car")
        >>> t.insert("cart")
        >>> t.insert("cast")
        >>> t
        ROOT
        └─┬ c
          └─┬ a
            ├─┬ r ✓
            │ └── t ✓
            └─┬ s
              └── t ✓
        >>> t.has_prefix("car")
        True
        >>> t.has_prefix("cas")
        True
        >>> "cas" in t
        False
        """
        if type(prefix) != str:
            return False
        last_node, remaining = self._follow_path(prefix)
        if remaining:
            child = last_node.get_child(remaining[0])
            child_data = child.get_data() if child else ""
            return child_data[: len(remaining)] == remaining
        return True

    # =============================    INSERT    ==============================
    def insert(self, word):
        """
        Inserts a `word` in the `Trie()` instance.

        Parameters
        ----------
        word: str
            The new word that will be inserted.

        Raises
        ------
        ValueError:
            If the given `word` is empty.
        TypeError:
            If the type of the given `word` is not `str`.

        Example
        -------
        >>> t = Trie()
        >>> t.insert("car")
        >>> t.insert("cart")
        >>> t.insert("cast")
        >>> t
        ROOT
        └─┬ c
          └─┬ a
            ├─┬ r ✓
            │ └── t ✓
            └─┬ s
              └── t ✓
        """
        self._validate_item(word, accept_empty_string=False)
        last_node, remaining_word = self._follow_path(word)
        curr_node = last_node
        for ch in remaining_word:
            child = TrieNode(ch)
            curr_node.set_child(ch, child)
            self._nodes_count += 1
            curr_node = child
        curr_node._is_word = True

    # =============================    REMOVE    ==============================
    def remove(self, word):
        """
        Removes the given `word` from the `Trie()` instance.

        Parameters
        ----------
        word: str
            The word to be deleted from the `Trie()`.

        Raises
        ------
        UserWarning:
            If the `Trie()` instance is empty of if the value wasn't found in
            the instance.

        Example
        -------
        >>> t = Trie()
        >>> t.insert("car")
        >>> t.insert("cart")
        >>> t.insert("cast")
        >>> t
        ROOT
        └─┬ c
          └─┬ a
            ├─┬ r ✓
            │ └── t ✓
            └─┬ s
              └── t ✓
        >>> t.remove("cart")
        ROOT
        └─┬ c
          └─┬ a
            ├── r ✓
            └─┬ s
              └── t ✓
        """
        if type(word) != str:
            warnings.warn(
                f"`{word}` doesn't exist in `{self.__name__}`",
                UserWarning
            )
            return
        elif word == "":
            return
        last_node, remaining_word = self._follow_path(word)
        if remaining_word == "":  # found the whole word
            curr_node = last_node
            curr_node._is_word = False
            while not curr_node._is_word and curr_node.is_leaf():
                ch = curr_node.get_data()[0]
                parent = curr_node.get_parent()
                del parent._children[ch]
                self._nodes_count -= 1
                curr_node = parent

    def clear(self):
        """
        Removes all nodes within the `Trie()` instance in constant time.

        Example
        -------
        >>> t = Trie()
        >>> t.insert("car")
        >>> t.insert("cart")
        >>> t.insert("cast")
        >>> t
        ROOT
        └─┬ c
          └─┬ a
            ├─┬ r ✓
            │ └── t ✓
            └─┬ s
              └── t ✓
        >>> t.clear()
        >>> t
        --
        >>> t.is_empty()
        True
        """
        super().clear()

    # ============================= AUTOCOMPLETE ==============================
    def _get_candidates(self, start_node, prev_prefixes):
        """
        A helper method to the auto-complete() method.
        """
        assert isinstance(start_node, TrieNode)
        assert type(prev_prefixes) == list

        output = []
        prefixes = prev_prefixes + [start_node.get_data()]
        if start_node._is_word:
            output.append("".join(prefixes))
        # iterate over children
        for child in start_node.get_children():
            output.extend(self._get_candidates(child, prefixes))
        return output

    def auto_complete(self, prefix=""):
        """
        Parses the `Trie()` instance and retrieves all the words that has the
        given `prefix`. In other words, auto-compeletes a given prefix using
        all saved words found in the `Trie()` instance.

        Parameters
        ----------
        prefix: str (default '')
            A prefix to auto-complete.

        Returns
        -------
        list:
            A list of all found words that have the given `prefix`.

        Example
        -------
        >>> t = Trie()
        >>> t.insert("car")
        >>> t.insert("cart")
        >>> t.insert("cast")
        >>> t
        ROOT
        └─┬ c
          └─┬ a
            ├─┬ r ✓
            │ └── t ✓
            └─┬ s
              └── t ✓
        >>> t.auto_complete("car")
        ["car", "cart"]
        >>> t.auto_complete("cas")
        ["cast"]
        >>> t.auto_complete()
        ['car', 'cart', 'cast']

        Note
        ----
        Using an empty prefix as an input will return all saved words in the
        `Trie()` instance.
        """
        self._validate_item(prefix)
        last_node, remaining = self._follow_path(prefix)
        candidates = []
        if remaining == "":
            curr_node = last_node
            # get candidates starting from given prefix
            if curr_node._is_word:
                candidates.append(prefix)
            for child in curr_node.get_children():
                candidates.extend(self._get_candidates(child, [prefix]))
        return candidates

    # =============================     NODES    ==============================
    def get_nodes_per_level(self):
        """
        Retrieves all trie nodes within the `Trie()` instance so that all
        trie nodes in a certain level will be concatenated into a separate
        list.

        Returns
        -------
        list:
            A nested list where the first inner-list has all the trie nodes in
            the first level, the second inner-list has all the trie nodes in
            the second level, ... so on.

        Example
        -------
        >>> t = Trie()
        >>> t.insert("car")
        >>> t.insert("cart")
        >>> t.insert("cast")
        >>> t
        ROOT
        └─┬ c
          └─┬ a
            ├─┬ r ✓
            │ └── t ✓
            └─┬ s
              └── t ✓
        >>> t.get_nodes_per_level()
        [['c'], ['a'], ['r', 's'], ['t', 't']]
        """
        return super().get_nodes_per_level()[1:]
