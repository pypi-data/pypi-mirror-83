"""
Red-Black Tree is a self-balancing BST (Binary Search Tree) which means that
it has a guaranteed height of **O(log(n))** where **n** is the number of nodes
within the tree. Each node in the Red-Black Tree has a color, this color is
either "Red" or "Black". Hence, the name "Red-Black Tree". The color of the
node is used only to re-balance the tree and has nothing to do with anything
else.

So, the following is a simple Red-Black Tree:

.. code-block:: text

               ______13|B______
              /                \\
       _____8|R_             __17|R______
      /         \\          /             \\
    1|B_        11|B      15|B         __25|B
        \\                            /
        6|R                         22|R


As we can see, the previous Red-Black Tree is a Bineary Search Tree with an
additional color denoted by either **R** for "red" or **B** for "black". In
addition to the BST characteristics, Red-black trees have these additional
characteristics:

- A node is either 'red' or 'black'.
- Root is always 'black'.
- A node is 'red' if it has two 'black' children.
- Any child of a red-node is always 'black'.
- **Black depth**: is the depth of all black nodes.All nodes with zero or one \
    children have the same black depth.
- **Shortest path**: It is the path from the root to the nearest leaf-node \
    and it is equal to the black depth.
- **Longest path**: It is the path from the root to the furthest leaf-node \
    with alternating red and black nodes. And it can't be bigger than \
    (2*shortest-path).
"""
import warnings
from enum import Enum
from extra.trees.bst import BSTNode, BST


class Color(Enum):
    BLACK = 0
    RED = 1


class RedBlackNode(BSTNode):
    """
    A red-black node is the basic unit for building Red-Black Trees. A red-
    black node must contain a number and a color; this color can be either
    "red" or "black" based on the node's position in the tree. Each red-black
    tree node has either zero, one or two children red-black nodes.
    """

    __name__ = "extra.RedBlackNode()"

    def __init__(self, value, color=Color.RED):
        """
        Creates a `RedBlackNode()` object which is the basic unit for building
        `RedBlackTree()` objects!!

        Parameters
        ----------
        value: int or float
            The value to be saved within the `BSTNode()` instance.
        color: Enum (default:Color.RED)
            The color of the node, it can be either `Color.RED` or
            `Color.BLACK`.

        Raises
        ------
        TypeError:
            If the given `value` isn't a number.
        ValueError:
            This can be raised in two cases:
                1. If the given `value` is `None`.
                2. If the given color is neither `Color.RED` nor `Color.BLACK`.
        """
        if color not in {Color.RED, Color.BLACK}:
            raise ValueError(f"Invalid color for `{self.__name__}`!!")
        super().__init__(value)
        self._color = color

    def get_color(self):
        """
        Returns the color of the current `RedBlackNode()` instance.

        Returns
        -------
        Enum:
            The color of the current `RedBlackNode()`.
        """
        return self._color

    def set_color(self, new_color):
        """
        Sets the given color as the color of the current `RedBlackNode()`.

        Parameters
        ----------
        new_color: Color
            The new color of the current `RedBlackNode()`.

        Raises
        ------
        ValueError:
            If the given color is neither `Color.RED` nor `Color.BLACK`.
        """
        if new_color not in {Color.RED, Color.BLACK}:
            raise ValueError(f"Invalid color for `{self.__name__}`!!")
        self._color = new_color

    def __repr__(self):
        """
        Represents `RedBlackNode()` object as a string.

        Returns
        -------
        str:
            A string representing the `RedBlackNode()` instance.

        Example
        -------
        >>> x = RedBlackNode(10)
        >>> x
        RedNode(10)
        >>>
        >>> x = RedBlackNode(10, color=Color.BLACK)
        >>> x
        BlackNode(10)
        """
        if self._color == Color.RED:
            return f"RedNode({self._data})"
        elif self._color == Color.BLACK:
            return f"BlackNode({self._data})"

    def _represent(self):
        """
        A helpful function used to represent the node when printing!!

        Returns
        -------
        str:
            A string representing the `RedBlackNode()` is a very simple way.

        Example
        -------
        >>> x = RedBlackNode(10)
        >>> x
        RedNode(10)
        >>> x._represent()
        10
        >>>
        >>> x = RedBlackNode(10, color=Color.BLACK)
        >>> x
        >>> BlackNode(10)
        >>> x._represent()
        10
        >>> type(x._represent())
        <class 'str'>
        """
        if self._color == Color.RED:
            return str(self._data) + "|R"
        elif self._color == Color.BLACK:
            return str(self._data) + "|B"

    @staticmethod
    def swap(node1, node2):
        """
        A static method to swap the data within the given two `RedBlackNode()`
        instances along with the nodes' color.

        Parameters
        ----------
        node1: TreeNode()
            The first `TreeNode()` instance whose data should be swapped.
        node2: TreeNode()
            The second `TreeNode()` instance whose data should be swapped.

        Raises
        ------
        TypeError:
            If one of the given instances isn't a `RedBlackNode()`.

        Example
        -------
        >>> x = RedBlackNode(10, color=Color.BLACK)
        >>> y = RedBlackNode(20)
        >>>
        >>> RedBlackNode.swap(x, y)
        >>> x
        RedNode(20)
        >>> y
        BlackNode(10)
        >>>
        >>> TreeNode.swap(x, 10)
        TypeError: Incompitable objects' type preventing swapping!!
        """
        # node1._data, node2._data = node2._data, node1._data
        super().swap(node1, node2)
        node1._color, node2._color = node2._color, node1._color


class RedBlackTree(BST):
    """
    Red-Black Tree is a self-balancing BST (Binary Search Tree) which means
    that it has a guaranteed height of **O(log(n))** where **n** is the number
    of nodes within the tree. Each node in the Red-Black Tree has a color, this
    color is either "Red" or "Black". Hence, the name "Red-Black Tree". The
    color of the node is used only to re-balance the tree and has nothing to do
    with anything else.
    """

    _basic_node = RedBlackNode
    __name__ = "extra.RedBlackTree()"

    def __init__(self, iterable=None):
        """
        A class method which creates a `RedBlackTree()` instance using an
        iterable in time-complexity of O(n) where **n** is the number of
        elements inside the given `iterable`.

        Parameters
        ----------
        iterable: iterable (default: None)
            An iterable python object that implements the `__iter__` method.
            For example, `list` and `tuple` are both iterables.

        Raises
        ------
        TypeError:
            It can be raised in three cases
                1. In case the given object isn't iterable.
                2. If one of the elements in the iterable is an `Extra` object.
                3. If one of the elements in the iterable is NOT a number.
        ValueError:
            If one of the iterable elements is `None`.

        Examples
        --------
        >>> rbtree = RedBlackTree([13, 8, 17, 1, 11, 15, 25, 6])
        >>> rbtree
                   ______13|B______
                  /                \\
           _____8|R_             __17|B_
          /         \\          /       \\
        1|B_        11|B      15|R      25|R
            \\
            6|R

        Using an iterable object with `None` as one of its elements will raise
        `ValueError`

        >>> RedBlackTree([2, None])
        ValueError: Can't use `None` as an element within \
`extra.RedBlackTree()`!!

        Using a non-iterable object will raise `TypeError`

        >>> RedBlackTree(2)
        TypeError: The given object isn't iterable!!

        Using nested `RedBlackTree()` objects will raise `TypeError` as well

        >>> rbtree_1 = RedBlackTree([1])
        >>> rbtree_2 = RedBlackTree([1, rbtree_1])
        TypeError: Can't create `extra.RedBlackTree()` using \
`extra.RedBlackTree()`!!
        """
        super().__init__(iterable)

    # =============================    LENGTH    ==============================
    def __len__(self):
        """
        Gets the length of the `RedBlackTree()` instance in constant time.

        Returns
        -------
        int:
            The length of the `RedBlackTree()` instance. Length is the number
            of red-black nodes in the instance.

        Example
        -------
        >>> rbtree = RedBlackTree([13, 8, 17, 1, 11, 15, 25, 6])
        >>> rbtree
                   ______13|B______
                  /                \\
           _____8|R_             __17|B_
          /         \\          /       \\
        1|B_        11|B      15|R      25|R
            \\
            6|R
        >>> len(rbtree)
        7
        """
        return self._length

    def is_empty(self):
        """
        Checks if the `RedBlackTree()` instance is empty or not in constant
        time.

        Returns
        -------
        bool:
            A boolean flag showing if the `RedBlackTree()` instance is empty or
            not. `True` shows that this instance is empty and `False` shows
            it's not empty.

        Example
        --------
        >>> rbtree = RedBlackTree()
        >>> rbtree.is_empty()
        True
        >>> rbtree.insert(10)
        >>> rbtree.is_empty()
        False
        """
        return super().is_empty()

    # =============================   MIN/MAX    ==============================
    def get_max(self):
        """
        Gets the maximum value in the `RedBlackTree()` isntance. The maximum
        value can be found at the right-most tree node in the `RedBlackTree()`
        instance.

        Returns
        -------
        int or float:
            The maximum numeric value in the `RedBlackTree()` instance.

        Raises
        ------
        IndexError:
            In case the `RedBlackTree()` instance is empty.

        Example
        -------
        >>> rbtree = RedBlackTree([13, 8, 17, 1, 11, 15, 25, 6])
        >>> rbtree
                   ______13|B______
                  /                \\
           _____8|R_             __17|B_
          /         \\          /       \\
        1|B_        11|B      15|R      25|R
            \\
            6|R
        >>> rbtree.get_max()
        25
        """
        return super().get_max()

    def get_min(self):
        """
        Gets the minimum value in the `RedBlackTree()` isntance. The minimum
        value can be found at the left-most tree node in the `RedBlackTree()`
        instance.

        Returns
        -------
        int or float:
            The minimum numeric value in the `RedBlackTree()` instance.

        Raises
        ------
        IndexError: In case the `RedBlackTree()` instance is empty.

        Example
        -------
        >>> rbtree = RedBlackTree([13, 8, 17, 1, 11, 15, 25, 6])
        >>> rbtree
                   ______13|B______
                  /                \\
           _____8|R_             __17|B_
          /         \\          /       \\
        1|B_        11|B      15|R      25|R
            \\
            6|R
        >>> rbtree.get_min()
        1
        """
        return super().get_min()

    # =============================    SEARCH    ==============================
    def __contains__(self, find_val):
        """
        Searches the `RedBlackTree()` for the given value and returns `True` if
        the value exists and `False` if not.

        Parameters
        ----------
        find_val: int or float
            The value to be searched for in the `RedBlackTree()` instance.

        Returns
        -------
        bool:
            Returns `True` if the value exists in the `RedBlackTree()` instance
            and False` if not.

        Example
        -------
        >>> rbtree = RedBlackTree([13, 8, 17, 1, 11, 15, 25, 6])
        >>> rbtree
                   ______13|B______
                  /                \\
           _____8|R_             __17|B_
          /         \\          /       \\
        1|B_        11|B      15|R      25|R
            \\
            6|R
        >>> 17 in rbtree
        True
        >> 50 in rbtree
        False
        """
        return super().__contains__(find_val)

    # =============================    RECOLOR   ==============================
    def __recolor_case3(self, start_node):
        """
        Recolors the `RedBlackTree()` instance when the parent of the given
        `start_node` is 'red' and uncle is 'black'.

        Parameters
        ----------
        start_node: RedBlackNode()
            A reference to the root of the subtree at which recoloring begins.

        Returns
        -------
        RedBlackNode():
            A reference to the same given `start_node` after recoloring the
            whole subtree.

        Raises
        ------
        AssertionError:
            If the given `start_node` isn't a `RedBlackNode()`.
        """
        assert isinstance(start_node, self._basic_node)

        # get basic info
        parent = start_node.get_parent()
        grandparent = parent.get_parent() if parent else None
        # parent is left-child and start_node is left-child
        if parent.is_left_child() and start_node.is_left_child():
            grandparent.set_color(Color.RED)
            parent.set_color(Color.BLACK)
            grandparent = super()._rotate_right(grandparent)
        # parent is left-child and start_node is right-child
        elif parent.is_left_child() and not start_node.is_left_child():
            # first rotation
            parent = super()._rotate_left(parent)
            grandparent.set_left(parent)
            grandparent.set_color(Color.RED)
            # second rotation
            grandparent = super()._rotate_right(grandparent)
            grandparent.set_color(Color.BLACK)
        # parent is right-child and start_node is left-child
        elif not parent.is_left_child() and start_node.is_left_child():
            # first rotation
            parent = super()._rotate_right(parent)
            grandparent.set_right(parent)
            grandparent.set_color(Color.RED)
            # second rotation
            grandparent = super()._rotate_left(grandparent)
            grandparent.set_color(Color.BLACK)
        # parent is right-child and start_node is right-child
        else:
            grandparent.set_color(Color.RED)
            parent.set_color(Color.BLACK)
            grandparent = super()._rotate_left(grandparent)
        return grandparent

    def __recolor(self, start_node):
        """
        Recolors the `RedBlackTree()` instance after insertion or removal. When
        recoloring, there are three different cases that can be discussed:

        - case I:   parent is 'black'
        - case II:  parent is 'red' and uncle is 'red'
        - case III: parent is 'red' and uncle is 'black'

        Parameters
        ----------
        start_node: RedBlackNode()
            A reference to the root of the subtree at which recoloring begins.

        Returns
        -------
        RedBlackNode():
            A reference to the same given `start_node` after recoloring the
            whole subtree.

        Raises
        ------
        AssertionError:
            If the given `start_node` isn't a `RedBlackNode()`.
        """
        assert isinstance(start_node, self._basic_node)

        # get basic info
        uncle = start_node.get_uncle()
        parent = start_node.get_parent()
        grandparent = parent.get_parent() if parent else None
        # recolor when node has a grandparent
        if parent is None or grandparent is None:
            return parent if parent else start_node

        # case I
        if parent.get_color() == Color.BLACK:
            # do nothing
            # print("Case I")
            return self._root
        else:
            # case II
            if uncle and uncle.get_color() == Color.RED:
                # print("Case II")
                parent.set_color(Color.BLACK)
                uncle.set_color(Color.BLACK)
                grandparent.set_color(Color.RED)
            # case III
            else:
                # print("Case III")
                # get great grandparent
                great_grandparent = grandparent.get_parent()
                grandparent = self.__recolor_case3(start_node)
                # set connection
                if great_grandparent:
                    if great_grandparent.get_data() > grandparent.get_data():
                        great_grandparent.set_left(grandparent)
                    else:
                        great_grandparent.set_right(grandparent)
            # recursively do the same over grandparent
            return self.__recolor(grandparent)

    # =============================    INSERT    ==============================
    def insert(self, value):
        """
        Inserts a numeric value in the `RedBlackTree()` instance according to
        the rules of binary search trees and the rules red-black trees as well.

        Parameters
        ----------
        value: int or float
            The new numeric value that will be inserted.

        Raises
        ------
        ValueError:
            If the given `value` is `None`.
        TypeError:
            If either the given `value` is not a numeric value.

        Example
        -------
        >>> rbtree = RedBlackTree()
        >>> rbtree.insert(10)
        >>> rbtree.insert(5)
        >>> rbtree.insert(15)
        >>> rbtree
           _10|B_
          /      \\
        5|R      15|R
        >>> rbtree.insert("2")
        TypeError: `extra.RedBlackTree()` accepts only numbers!!
        """
        super()._validate_item(value)
        if self.is_empty():
            self._root = self._basic_node(value)
            self._root.set_color(Color.BLACK)
            self._length += 1
        else:
            # insert new node
            new_node = super()._insert(value)
            # recolor starting from new_node till root
            self._root = self.__recolor(new_node)
            # root is always black (isn't essential tho!!)
            self._root.set_color(Color.BLACK)

    # =============================    REMOVAL   ==============================
    def _find_replacement(self, node):
        """
        Find a replacement to the numeric value of the given `node` as a
        preparation step before removing `node`. This replacement will be
        either the in-order predecessor or the in-order successor.

        Parameters
        ----------
        node: RedBlackNode()
            The node that will be replaced.

        Returns
        -------
        RedBlackNode():
            The node that will replace the given `node`.

        Raises
        ------
        AssertionError:
            If the given `node` isn't a `RedBlackNode()` object.

        Example
        -------
        >>> rbtree = RedBlackTree([13, 8, 17, 1, 11, 15, 25, 6])
        >>> rbtree
                   ______13|B______
                  /                \\
           _____8|R_             __17|B_
          /         \\          /       \\
        1|B_        11|B      15|R      25|R
            \\
            6|R
        >>> rbtree._find_replacement(rbtree._root)
        RedNode(15)
        >>> rbtree._find_replacement(rbtree._root._left)
        RedNode(6)

        Note
        ----
        Here, we're tyring to exploit two characteristics of Red-black
        trees and they are:

            1. Red nodes are good replacements.
            2. When removing a red node, there must be at least one red-node
            as a replacement.
        """
        assert isinstance(node, RedBlackNode)
        if node.is_leaf():
            replacement_node = None
        else:
            # in-order successor
            successor = (
                super()._get_min_node(node.get_right())
                if node.get_right()
                else None
            )
            # in-order predecessor
            predecessor = (
                super()._get_max_node(node.get_left())
                if node.get_left()
                else None
            )
            # find the red-node
            if successor and successor.get_color() == Color.RED:
                replacement_node = successor
            elif predecessor and predecessor.get_color() == Color.RED:
                replacement_node = predecessor
            else:
                replacement_node = successor if successor else predecessor
        return replacement_node

    def __handle_double_black(self, parent, double_black_node):
        """
        Recolors a double-black node. A double-black node is a black node that
        turns to double-black node after removing a red node child which causes
        this node to be double black in order to keep the red-black tree
        properties intact. This private methods handles that case and converts
        it to a black node after some other changes.

        Parameters
        ----------
        parent: RedBlackNode()
            A reference to the parent of the double-black node.
        double_black_node: RedBlackNode()
            A reference to the double-black node.

        Raises
        ------
        AssertionError:
            If the given `node` or its parent isn't a `RedBlackNode()` object.

        Note
        ----
        When dealing with double black nodes, we have four cases:

        - Case I  : The double_black_node is the root.
        - Case II : The sibling is black and one child of the sibling's \
            children is red.
        - Case III: The sibling is black and the two children of the sibling \
            are black.
        - Cae IV : The sibling is red.

        SRC: https://www.programiz.com/dsa/deletion-from-a-red-black-tree
        """
        # TODO: should be refactored
        assert isinstance(parent, RedBlackNode)
        assert (
            double_black_node is None
            or isinstance(double_black_node, RedBlackNode)
        )

        while double_black_node != self._root and (
            not double_black_node
            or double_black_node.get_color() == Color.BLACK
        ):
            # double black node is the left-child
            if double_black_node == parent.get_left():
                sibling = parent.get_right()
                # Case IV
                if sibling and sibling.get_color() == Color.RED:
                    sibling.set_color(Color.BLACK)
                    parent.set_color(Color.RED)
                    grandparent = parent.get_parent()
                    parent = super()._rotate_left(parent)
                    super()._attach(grandparent, parent)
                    # update parent and sibling
                    parent = parent.get_left()
                    sibling = parent.get_right()
                # check sibling children
                s_left_child = sibling.get_left()
                s_right_child = sibling.get_right()
                # get colors of sibling's children
                s_left_color = (
                    s_left_child.get_color() if s_left_child else Color.BLACK
                )
                s_right_color = (
                    s_right_child.get_color() if s_right_child else Color.BLACK
                )
                # Case III
                if (s_left_color == Color.BLACK
                        and s_right_color == Color.BLACK):
                    sibling.set_color(Color.RED)
                    double_black_node = parent
                # Case II
                else:
                    if s_right_color == Color.BLACK:
                        s_left_child.set_color(Color.BLACK)
                        sibling.set_color(Color.RED)
                        sibling = super()._rotate_right(sibling)
                        super()._attach(parent, sibling)
                        sibling = parent.get_right()

                    sibling.set_color(parent.get_color())
                    parent.set_color(Color.BLACK)
                    s_right_child = sibling.get_right()
                    s_right_child.set_color(Color.BLACK)
                    grandparent = parent.get_parent()
                    parent = super()._rotate_left(parent)
                    super()._attach(grandparent, parent)
                    double_black_node = self._root
            # ===== Mirror image of the previous if-condition =====
            # double black node is the right-child
            else:
                sibling = parent.get_left()
                # Case IV
                if sibling and sibling.get_color() == Color.RED:
                    sibling.set_color(Color.BLACK)
                    parent.set_color(Color.RED)
                    grandparent = parent.get_parent()
                    parent = super()._rotate_right(parent)
                    super()._attach(grandparent, parent)
                    # update parent and sibling
                    parent = parent.get_right()
                    sibling = parent.get_left()
                # check sibling children
                s_left_child = sibling.get_left()
                s_right_child = sibling.get_right()
                # get colors of sibling's children
                s_left_color = (
                    s_left_child.get_color() if s_left_child else Color.BLACK
                )
                s_right_color = (
                    s_right_child.get_color() if s_right_child else Color.BLACK
                )
                # Case III
                if (s_right_color == Color.BLACK
                        and s_right_color == Color.BLACK):
                    sibling.set_color(Color.RED)
                    double_black_node = parent
                # Case II
                else:
                    if s_left_color == Color.BLACK:
                        s_right_child.set_color(Color.BLACK)
                        sibling.set_color(Color.RED)
                        sibling = super()._rotate_left(sibling)
                        super()._attach(parent, sibling)
                        sibling = parent.get_left()

                    sibling.set_color(parent.get_color())
                    parent.set_color(Color.BLACK)
                    s_left_child = sibling.get_left()
                    s_left_child.set_color(Color.BLACK)
                    grandparent = parent.get_parent()
                    parent = super()._rotate_right(parent)
                    super()._attach(grandparent, parent)
                    double_black_node = self._root
        # make sure root is always black
        self._root.set_color(Color.BLACK)

    def remove(self, del_value):
        """
        Removes the `del_value` from the `RedBlackTree()` instance which is one
        of the following cases:

        - Case I  : The removed node is 'red', and its replacement is either \
            'red' or None.
        - Case II : The removed node is 'red', and its replacement is 'black'.
        - Case III: The removed node is 'black', and its replacement is \
            either 'black' or None.
        - Case IV : The removed node is 'black', and its replacement is 'red'.

        Parameters
        ----------
        del_value: int or float
            The value to be deleted from the `RedBlackTree()`.

        Raises
        ------
        UserWarning:
            If the `RedBlackTree()` instance is empty of if the value wasn't
            found in the instance.

        Example
        -------
        >>> rbtree = RedBlackTree([13, 8, 17, 1, 11, 15, 25, 6])
        >>> rbtree
                   ______13|B______
                  /                \\
           _____8|R_             __17|B_
          /         \\          /       \\
        1|B_        11|B      15|R      25|R
            \\
            6|R
        >>> rbtree.remove(13)
        >>> rbtree
                   ______15|B_
                  /           \\
           _____8|R_          17|B_
          /         \\             \\
        1|B_        11|B           25|R
            \\
            6|R
        >>> rbtree.remove(50)
        UserWarning: Couldn't find `50` in `extra.RedBlackTree()`!!
        """

        # check edge case
        if self.is_empty():
            warnings.warn(f"`{self.__name__}` is empty!!", UserWarning)
            return
        elif type(del_value) not in {int, float}:
            warnings.warn(
                f"Couldn't find `{del_value}` in `{self.__name__}`!!",
                UserWarning
            )
            return
        elif self._root.is_leaf() and del_value == self._root.get_data():
            self._root = None
            self._length -= 1
            return

        # search for the del_value node
        removed_node = super()._search(del_value, self._root)
        # couldn't find the node
        if removed_node.get_data() != del_value:
            warnings.warn(
                f"Couldn't find `{del_value}` in `{self.__name__}`!!",
                UserWarning
            )
            return
        # find replacement
        replacement = self._find_replacement(removed_node)
        # print("replacement:", replacement)

        # Case I (replace red-node with red-node/None)
        if removed_node.get_color() == Color.RED and (
            replacement is None or replacement.get_color() == Color.RED
        ):
            # print("Case I (replace red-node with red-node/None)")
            super()._transplant(removed_node, replacement)

        # Case II (replace red-node with black-node)
        elif (
            removed_node.get_color() == Color.RED
            and replacement.get_color() == Color.BLACK
        ):
            # print("Case II (replace red-node with black-node)")
            raise ValueError("Debug this, this case shouldn't occur!!")

        # Case III (replace black-node with black-node)
        elif removed_node.get_color() == Color.BLACK and (
            replacement is None or replacement.get_color() == Color.BLACK
        ):
            # print("Case III (double black-node)")
            if replacement:
                parent = replacement.get_parent()
            else:
                parent = removed_node.get_parent()
            # do the transplant
            super()._transplant(removed_node, replacement)
            # get double black node
            if replacement is None:
                if parent.get_left() is None:
                    double_black_node = parent.get_left()
                else:
                    double_black_node = parent.get_right()
            else:
                if replacement.get_data() < parent.get_data():
                    double_black_node = parent.get_left()
                else:
                    double_black_node = parent.get_right()
            # handle this double black
            self.__handle_double_black(parent, double_black_node)

        # Case IV (replace black-node with red-node/None)
        elif (
            removed_node.get_color() == Color.BLACK
            and replacement.get_color() == Color.RED
        ):
            replacement.set_color(Color.BLACK)
            # print("Case IV (replace black-node with red-node/None)")
            super()._transplant(removed_node, replacement)
        # decrease the length
        self._length -= 1

    def clear(self):
        """
        Removes all nodes within the `RedBlackTree()` instance in constant
        time.

        Example
        -------
        >>> rbtree = RedBlackTree([13, 8, 17, 1, 11, 15, 25, 6])
        >>> rbtree
                   ______13|B______
                  /                \\
           _____8|R_             __17|B_
          /         \\          /       \\
        1|B_        11|B      15|R      25|R
            \\
            6|R
        >>> rbtree.clear()
        >>> rbtree
        / \\
        >>> rbtree.is_empty()
        True
        """
        super().clear()

    # ============================= HEIGHT/DEPTH ==============================
    def get_black_height(self):
        """
        Gets the black height of the `RedBlackTree()` instance. The black
        height is the number of black nodes; starting from the root till any
        leaf node knowing that the root node (which is always black) is not
        counted.

        Returns
        -------
        int:
            A positive integer representing the black height of the instance.

        Example
        -------
        >>> rbtree = RedBlackTree([13, 8, 17, 1, 11, 15, 25, 6])
        >>> rbtree
                   ______13|B______
                  /                \\
           _____8|R_             __17|B_
          /         \\          /       \\
        1|B_        11|B      15|R      25|R
            \\
            6|R
        >>> rbtree.get_black_height()
        2
        """
        black_height = 0
        start_node = self._root.get_left()
        while start_node is not None:
            if start_node.get_color() == Color.BLACK:
                black_height += 1
            start_node = start_node.get_left()
        # +1 to include NIL node
        return black_height + 1

    def get_height(self):
        """
        Gets the height of the `RedBlackTree()` instance. The RedBlackTree's
        height is the number of edges between the root and the furthest leaf
        node.

        Returns
        -------
        int:
            A positive integer representing the height of the instance.

        Example
        -------
        >>> rbtree = RedBlackTree([13, 8, 17, 1, 11, 15, 25, 6])
        >>> rbtree
                   ______13|B______
                  /                \\
           _____8|R_             __17|B_
          /         \\          /       \\
        1|B_        11|B      15|R      25|R
            \\
            6|R
        >>> rbtree.get_height()
        3
        """
        return super().get_height()

    def get_depth(self):
        """
        Gets the depth of the `RedBlackTree()` instance.

        Returns
        -------
        int:
            A positive integer representing the depth of the instance.

        Example
        -------
        >>> rbtree = RedBlackTree([13, 8, 17, 1, 11, 15, 25, 6])
        >>> rbtree
                   ______13|B______
                  /                \\
           _____8|R_             __17|B_
          /         \\          /       \\
        1|B_        11|B      15|R      25|R
            \\
            6|R
        >>> rbtree.get_depth()
        0
        """
        return super().get_depth()

    # =============================  LEAF NODES  ==============================
    def count_leaf_nodes(self):
        """
        Counts the number of leaf nodes in the `RedBlackTree()` instance. Leaf
        nodes are the tree nodes that have no children.

        Returns
        -------
        int:
            A positive integer representing the number of leaf nodes in the
            `RedBlackTree()`.

        Example
        -------
        >>> rbtree = RedBlackTree([13, 8, 17, 1, 11, 15, 25, 6])
        >>> rbtree
                   ______13|B______
                  /                \\
           _____8|R_             __17|B_
          /         \\          /       \\
        1|B_        11|B      15|R      25|R
            \\
            6|R
        >>> rbtree.count_leaf_nodes()
        4
        """
        return super().count_leaf_nodes()

    # =============================    BALANCE   ==============================
    def is_balanced(self):
        """
        Checks if the `RedBlackTree()` instance is balanced. A RedBlackTree is
        balanced if the difference between the depth of any two leaf nodes is
        less than or equal to one.

        Returns
        -------
        bool:
            `True` if the `RedBlackTree()` instance is balanced and `False` if
            it is not balanced.

        Raises
        ------
        UserWarning:
            If the `RedBlackTree()` is empty.

        Example
        -------
        >>> rbtree = RedBlackTree([13, 8, 17, 1, 11, 15, 25, 6])
        >>> rbtree
                   ______13|B______
                  /                \\
           _____8|R_             __17|B_
          /         \\          /       \\
        1|B_        11|B      15|R      25|R
            \\
            6|R
        >>> rbtree.is_balanced()
        True
        """
        return super().is_balanced()

    # =============================    PERFECT   ==============================
    def is_perfect(self):
        """
        Checks if the `RedBlackTree()` instance is perfect. A RedBlackTree is
        perfect if all its levels are completely filled.

        Returns
        -------
        bool:
            `True` if the `RedBlackTree()` instance is perfect and `False` if
            it is not perfect.

        Raises
        ------
        UserWarning:
            If the `RedBlackTree()` is empty.

        Example
        -------
        >>> rbtree = RedBlackTree([13, 8, 17, 1, 11, 15, 25, 6])
        >>> rbtree
                   ______13|B______
                  /                \\
           _____8|R_             __17|B_
          /         \\          /       \\
        1|B_        11|B      15|R      25|R
            \\
            6|R
        >>> rbtree.is_perfect()
        False
        """
        return super().is_perfect()

    # =============================    STRICT    ==============================
    def is_strict(self):
        """
        Checks if the `RedBlackTree()` instance is strict. A RedBlackTree is
        strict if all its non-leaf nodes have two children (left and right).

        Returns
        -------
        bool:
            `True` if the `RedBlackTree()` instance is strict and `False` if
            it is not strict.

        Raises
        ------
        UserWarning:
            If the `RedBlackTree()` is empty.

        Example
        -------
        >>> rbtree = RedBlackTree([13, 8, 17, 1, 11, 15, 25, 6])
        >>> rbtree
                   ______13|B______
                  /                \\
           _____8|R_             __17|B_
          /         \\          /       \\
        1|B_        11|B      15|R      25|R
            \\
            6|R
        >>> rbtree.is_strict()
        False
        """
        return super().is_strict()

    # =============================     ITER     ==============================
    def __iter__(self):
        """
        Iterates over the `RedBlackTree()` instance and returns a generator of
        the `RedBlackNode()` values in breadth-first manner.

        Yields
        -------
        int or float:
            The number stored at each node in the instance.

        Example
        -------
        >>> rbtree = RedBlackTree([13, 8, 17, 1, 11, 15, 25, 6])
        >>> rbtree
                   ______13|B______
                  /                \\
           _____8|R_             __17|B_
          /         \\          /       \\
        1|B_        11|B      15|R      25|R
            \\
            6|R
        >>> for value in rbtree:
        ...     print(value, end=',')
        13,8,17,1,11,15,25,6,
        """
        return super().__iter__()

    def to_list(self):
        """
        Converts the `RedBlackTree()` instance to a `list` where values will
        be inserted in breadth-first manner.

        Returns
        -------
        list:
            A `list` object containing the same elements as the
            `RedBlackTree()` instance.

        Example
        -------
        >>> rbtree = RedBlackTree([13, 8, 17, 1, 11, 15, 25, 6])
        >>> rbtree
                   ______13|B______
                  /                \\
           _____8|R_             __17|B_
          /         \\          /       \\
        1|B_        11|B      15|R      25|R
            \\
            6|R
        >>> rbtree.to_list()
        [13, 8, 17, 1, 11, 15, 25, 6]
        """
        return super().to_list()

    # =============================     NODES    ==============================
    def get_nodes_per_level(self):
        """
        Retrieves all tree nodes within the `RedBlackTree()` instance so that
        all tree nodes in a certain level will be concatenated into a separate
        list.

        Returns
        -------
        list:
            A nested list where the first inner-list has all the tree nodes in
            the first level, the second inner-list has all the tree nodes in
            the second level, ... so on.

        Example
        -------
        >>> rbtree = RedBlackTree([13, 8, 17, 1, 11, 15, 25, 6])
        >>> rbtree
                   ______13|B______
                  /                \\
           _____8|R_             __17|B_
          /         \\          /       \\
        1|B_        11|B      15|R      25|R
            \\
            6|R
        >>> rbtree.get_nodes_per_level()
        [[13], [8, 17], [1, 11, 15, 25], [6]]
        """
        return super().get_nodes_per_level()

    # =============================  PRE-ORDER   ==============================
    def preorder_traverse(self):
        """
        Traverses the `RedBlackTree()` instance in pre-order manner. Which
        means that the **parent** is visited first. Then, the **left subtree**
        (if found), then the **right subtree** (if found).

        Note
        -----
        It's the same as `depth_first_traverse()` method.

        Returns
        --------
        list:
            A list of all values of the pre-order visited nodes.

        Example
        -------
        >>> rbtree = RedBlackTree([13, 8, 17, 1, 11, 15, 25, 6])
        >>> rbtree
                   ______13|B______
                  /                \\
           _____8|R_             __17|B_
          /         \\          /       \\
        1|B_        11|B      15|R      25|R
            \\
            6|R
        >>> rbtree.preorder_traverse()
        [13, 8, 1, 6, 11, 17, 15, 25]
        """
        return super().preorder_traverse()

    def depth_first_traverse(self):
        """
        Traverses the `RedBlackTree()` instance in depth-first manner. Which
        means that the **parent** is visited first. Then, the **left subtree**
        (if found), then the **right subtree** (if found).

        Note
        -----
        It's the same as `preorder_traverse()` method.

        Returns
        --------
        list:
            A list of all values of the pre-order visited nodes.

        Example
        -------
        >>> rbtree = RedBlackTree([13, 8, 17, 1, 11, 15, 25, 6])
        >>> rbtree
                   ______13|B______
                  /                \\
           _____8|R_             __17|B_
          /         \\          /       \\
        1|B_        11|B      15|R      25|R
            \\
            6|R
        >>> rbtree.depth_first_traverse()
        [13, 8, 1, 6, 11, 17, 15, 25]
        """
        return super().depth_first_traverse()

    # =============================  POST-ORDER  ==============================
    def postorder_traverse(self):
        """
        Traverses the `RedBlackTree()` instance in post-order manner. Which
        means that the **left subtree** (if found) is visited first. Then, the
        **right subtree** (if found) then the **parent**.

        Returns
        --------
        list:
            A list of all values of the pre-order visited nodes.

        Example
        -------
        >>> rbtree = RedBlackTree([13, 8, 17, 1, 11, 15, 25, 6])
        >>> rbtree
                   ______13|B______
                  /                \\
           _____8|R_             __17|B_
          /         \\          /       \\
        1|B_        11|B      15|R      25|R
            \\
            6|R
        >>> rbtree.postorder_traverse()
        [6, 1, 11, 8, 15, 25, 17, 13]
        """
        return super().postorder_traverse()

    # =============================   IN-ORDER   ==============================
    def inorder_traverse(self):
        """
        Traverses the `RedBlackTree()` instance in in-order manner. Which means
        that the **left subtree** (if found) is visited first. Then, the
        **parent** then the **right subtree** (if found).

        Returns
        --------
        list:
            A list of all values of the in-order visited nodes.

        Example
        -------
        >>> rbtree = RedBlackTree([13, 8, 17, 1, 11, 15, 25, 6])
        >>> rbtree
                   ______13|B______
                  /                \\
           _____8|R_             __17|B_
          /         \\          /       \\
        1|B_        11|B      15|R      25|R
            \\
            6|R
        >>> rbtree.inrder_traverse()
        [1, 6, 8, 11, 13, 15, 17, 25]
        """
        return super().inorder_traverse()

    # ============================= BREADTH-FIRST==============================
    def breadth_first_traverse(self):
        """
        Traverses the `RedBlackTree()` instance in breadth-first manner. Which
        means that the tree nodes will be visited level by level.

        Returns
        --------
        list:
            A list of all values of the pre-order visited nodes.

        Example
        -------
        >>> rbtree = RedBlackTree([13, 8, 17, 1, 11, 15, 25, 6])
        >>> rbtree
                   ______13|B______
                  /                \\
           _____8|R_             __17|B_
          /         \\          /       \\
        1|B_        11|B      15|R      25|R
            \\
            6|R
        >>> rbtree.breadth_first_traverse()
        [13, 8, 17, 1, 11, 15, 25, 6]
        """
        return super().breadth_first_traverse()

    # =============================   TRAVERSE   ==============================
    def traverse(self, method="inorder"):
        """
        Traversal is the process to visit all nodes of a RedBlackTree starting
        from the root as we cannot randomly access any node in a binary tree.
        There are four ways which we use to traverse a RedBlackTree:

        1. preorder - depth-first
        2. inorder
        3. posteorder
        4. breadth-first

        Parameters
        ----------
        method: str (default="inorder")
            A lower-cased string describing the type of traversal that will be
            used. It could be one of these values: ["inorder", "postorder",
            "preorder", "depth-first", "breadth-first"]

        Returns
        --------
        list:
            A list of all values of the visited nodes according to the
            specified traversal method.

        Raises
        ------
        ValueError:
            If the given method isn't known.
        TypeError:
            If the given method isn't a string.

        Example
        -------
        >>> rbtree = RedBlackTree([13, 8, 17, 1, 11, 15, 25, 6])
        >>> rbtree
                   ______13|B______
                  /                \\
           _____8|R_             __17|B_
          /         \\          /       \\
        1|B_        11|B      15|R      25|R
            \\
            6|R
        >>> rbtree.traverse("preorder")
        [13, 8, 1, 6, 11, 17, 15, 25]
        >>> rbtree.traverse("inorder")
        [1, 6, 8, 11, 13, 15, 17, 25]
        >>> rbtree.traverse("postorder")
        [6, 1, 11, 8, 15, 25, 17, 13]
        >>> rbtree.traverse("breadth-first")
        [13, 8, 17, 1, 11, 15, 25, 6]
        >>> rbtree.traverse("extra")
        ValueError: Given traverse method has to be one of these:
        {'breadth-first', 'postorder', 'inorder', 'depth-first', 'preorder'}
        """
        return super().traverse(method)
