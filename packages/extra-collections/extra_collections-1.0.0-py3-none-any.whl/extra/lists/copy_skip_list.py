import random
from extra.lists.doubly_linked_list import DoublyNode, DoublyLinkedList




#helper functions
random.seed(1)
def flip_coin():
    return random.choice(['head','tail'])


def search_sorted(start_node, value):
    # search a sorted linked list and return the last accessed node.
    prev = curr_node = start_node
    while(curr_node != None and curr_node.get_data() <= value):
        prev = curr_node
        curr_node = curr_node.get_next()
    return prev




class SkipNode(DoublyNode):
    def __init__(self, item):
        if type(item) not in {int, float}:
            raise TypeError("SkipNode uses only numbers!!")
        super().__init__(item)
        self.down = None


    def _represent(self):
        if self.data == float("-inf"):
            return "-∞"
        elif self.data == float("inf"):
            return "∞"
        return super()._represent()


    def get_down(self):
        return self.down
    

    def set_down(self, other_node):
        self.down = other_node




class SkipList:
    _basic_node = SkipNode


    def __name__(self):
        return "extra.SkipList()"
    

    def __init__(self):
        self.num_levels = 1
        #`level_listss` is an array of DoublyLinkedList objects
        self.level_lists = [DoublyLinkedList( self._basic_node(float("-inf")) )]


    def _validate_item(self, item):
        if type(item) not in {int, float}:
            raise TypeError(f"{self.__name__()} supports only numbers!!")
        

    def _validate_index(self, idx, accept_negative=False):
        if isinstance(idx, slice):
            raise NotImplementedError("Slices isn't supported yet!!")
        if type(idx) != int:
            raise TypeError("Given index must be an integer!")
        elif idx <= -1 and accept_negative==False:
            raise IndexError(\
                "Negative indexing isn't supported with this functinoality!!")
        elif idx < - len(self) or idx >= len(self):
            raise IndexError("Can't find any element at the given index!!")


    @classmethod
    def from_iterable(cls, iterable):
        if not hasattr(iterable, "__iter__"):
            raise TypeError("The given object isn't iterable!!")
        elif isinstance(iterable, cls):
            return iterable
        else:
            skiplist = cls()  #cls._create_instance(cls)
            for item in iterable:
                skiplist.insert(item)
            return skiplist
        

    ############################## PRINT ##############################
    def __print_node(self, node, zeroth_node, lower_node):
        """
        This private method is responsible for representing each node in the 
        Skip List. To do its job, it needs to use two other nodes:
        - zeroth_node: node of the 0th level of the Skip List where all nodes
            are represented.
        - lower_node: node of the lower level.
        """
        middle = []
        bottom_border = []
        item = zeroth_node._represent()
        width = len(item)+2 #2: for a space before & after an item
        if node != None and zeroth_node.get_data() == node.get_data():
            bottom_border += ['└'] if lower_node == None else ['├']
            bottom_border += (['─']*width)
            bottom_border += ['┘ '] if lower_node == None else ['┤ ']
            middle += [f"| {item} │⟷"]
        else:
            middle += [f"⟷{'⟷'*width}⟷⟷"]
            if lower_node != None and lower_node.data == zeroth_node.data:
                bottom_border += ['┌'] + (['─']*width) + ['┐ ']
            else:
                bottom_border += [' '] + ([' ']*width) + ['  ']
        return middle, bottom_border


    def __print_level(self, level):
        """
        This private method is responsible for representing each level in the 
        Skip List.
        NOTE: I know this isn't the best way to do it, but that's what popped up
        first into my mind.
        """
        assert level < self.num_levels
        zeroth_list = self.level_lists[0]
        curr_list = self.level_lists[level]
        # the following two lists will represent the output of this function
        bottom_border = []
        middle = []
        # iterate over two lists in parallel
        zeroth_node = zeroth_list.head
        curr_node = curr_list.head
        lower_node = self.level_lists[level-1].head if level > 0 else None
        while(zeroth_node != None):
            middle_part, bottom_part = \
                self.__print_node(curr_node, zeroth_node, lower_node)
            middle += middle_part
            bottom_border += bottom_part
            if curr_node != None and zeroth_node.data == curr_node.data:
                curr_node = curr_node.get_next()
            if lower_node != None and zeroth_node.data == lower_node.data:
                lower_node = lower_node.get_next()
            zeroth_node = zeroth_node.get_next()
        return "{}\n{}".format(''.join(middle), ''.join(bottom_border))


    def __print_top_border(self):
        """
        This method is only responsible for just one thing, to print out the 
        top border of the Skip List.
        """
        lower_list = self.level_lists[0]
        top_list = self.level_lists[self.num_levels-1]
        # the following two lists will represent the output of this function
        top_border = []
        # iterate over two lists in parallel
        lower_node = lower_list.head
        curr_node = top_list.head
        while(lower_node != None):
            item = lower_node._represent()
            width = len(item)+2 #2: for a space before & after an item
            if curr_node != None and lower_node.data == curr_node.data:
                top_border += ['┌'] + (['─']*width) + ['┐ ']
                curr_node = curr_node.get_next()
            else:
                top_border += [' '] + ([' ']*width) + ['  ']
            lower_node = lower_node.get_next()
        return "{}".format(''.join(top_border))


    def __repr__(self):
        """
        The complexity of this method is O(n*l) where:
            - n: is the number of nodes in the first list
            - l: is the number of levels
        Skip List is gonna look like this:
        ┌────┐                     ┌───┐
        │ -∞ │⟷⟷⟷⟷⟷⟷⟷⟷⟷⟷⟷⟷⟷⟷⟷⟷⟷⟷⟷⟷⟷│ 2 │⟷
        ├────┤        ┌────┐       ├───┤
        │ -∞ │⟷⟷⟷⟷⟷⟷⟷⟷│ 10 │⟷⟷⟷⟷⟷⟷⟷│ 2 │⟷
        ├────┤ ┌────┐ ├────┤ ┌───┐ ├───┤
        │ -∞ │⟷│ 77 │⟷│ 10 │⟷│ 6 │⟷│ 2 │⟷
        └────┘ └────┘ └────┘ └───┘ └───┘
        """
        output = [self.__print_top_border()]
        output += [self.__print_level(level) \
                    for level in range(self.num_levels-1, -1, -1)]
        return "\n".join(output)
    

    ############################## LENGTH ##############################    
    def __len__(self):
        return len(self.level_lists[0]) - 1
    

    def is_empty(self):
        return len(self) == 0


    ############################# ITERATOR #############################
    def __iter__(self):
        for item in self.level_lists[0][1:]:
            yield item.get_data()

    
    ############################## SEARCH ##############################
    def _search(self, value):
        # returns the last accessed node when searching a certain value.
        assert type(value) in {int, float}
        last_accessed_nodes = []
        top_list = self.level_lists[self.num_levels-1]
        start_node = top_list.head
        while(start_node.get_down() != None):
            found_node = search_sorted(start_node, value)
            if found_node.get_data() == value:
                return found_node, last_accessed_nodes
            last_accessed_nodes.append(found_node)
            start_node = found_node.get_down()
        found_node = search_sorted(start_node, value)
        assert len(last_accessed_nodes) == self.num_levels-1
        return found_node, last_accessed_nodes[::-1]


    def search(self, value):
        """Search Skip List is one in O(log(n)) time"""
        if type(value) not in {int, float}:
            return False
        self._validate_item(value)
        found_node, _ = self._search(value)
        return found_node.get_data() == value


    def __contains__(self, value):
        return self.search(value)
    

    def __getitem__(self, idx):
        self._validate_index(idx)
        #NOTE: idx+1 to skip -∞
        node = self.level_lists[0].__getitem__(idx+1)
        return node.get_data()


    ############################## INSERT ##############################
    def _add_extra_level(self):
        top_list = self.level_lists[self.num_levels-1]
        new_llist = DoublyLinkedList(self._basic_node(float("-inf")))
        # connect the head of the new linked list to the lower linked list
        new_llist.head.set_down(top_list.head)
        # add new linked list to the SkipList
        self.level_lists.append(new_llist)
        self.num_levels += 1
        return new_llist
    
    
    def _promote(self, upper_prev_node, curr_node, curr_level):
        assert isinstance(upper_prev_node, self._basic_node)
        assert isinstance(curr_node, self._basic_node)
        assert curr_level < self.num_levels
        # create new node with the same data as curr_data
        upper_node = self._basic_node(curr_node.get_data())
        # connect the upper list to the new node
        upper_node = self.level_lists[curr_level+1]._insert_node(
                                                    upper_prev_node, upper_node)
        # connect the current list with the upper one
        upper_node.set_down(curr_node)
        return upper_node


    def insert(self, value):
        """
        Inserts a value to our Skip List. Insertion is done in O(log(n)) time
        """
        self._validate_item(value)
        # search for that value
        found_node, last_accessed_nodes = self._search(value)
        # `value` already exists in our SkipList
        if found_node.get_data() == value:
            return
        # create new_node with the new value
        new_node = self._basic_node(value)
        # insert new_node to the 0th linkedlist
        curr_node = self.level_lists[0]._insert_node(found_node, new_node) 
        
        # promote the new_node if flipping the coin results `Head`
        curr_level = 0
        while flip_coin() == "head":
            if curr_level >= self.num_levels-1:
                top_list = self._add_extra_level()
                upper_prev_node = top_list.head
            else:
                upper_prev_node = last_accessed_nodes[curr_level]
            # promote new_node
            curr_node = self._promote(upper_prev_node, curr_node, curr_level)
            curr_level += 1

    
    ############################## REMOVE ##############################
    def _remove_level(self, level):
        assert type(level) == int and 1 <= level < self.num_levels
        del self.level_lists[level]
        self.num_levels -= 1
    

    def remove(self, value):
        """removal is done in O(log(n))"""
        if type(value) not in {int, float}:
            return
        self._validate_item(value)
        # search for that value
        found_node, last_accessed_nodes = self._search(value)
        #NOTE: len(last_accessed_nodes) can be used to get the level where
        #  this value was found
        if found_node.get_data() == value:
            level = self.num_levels - 1 - len(last_accessed_nodes)
            while(level >= 0):
                curr_level_list = self.level_lists[level]
                curr_level_list._remove_node(found_node.get_prev(), found_node)
                # check if curr_level_list is empty()
                if level != 0 and len(curr_level_list) == 1:
                    self._remove_level(level)
                level -= 1
                found_node = found_node.get_down()
    

    def __delitem__(self, idx):
        self._validate_index(idx)
        #NOTE: idx+1 to skip -∞
        _, node = self.level_lists[0]._get_node(idx+1)
        self.remove(node.get_data())
    

    def clear(self):
        self.__init__()
    

    ############################## MISC ##############################
    def to_list(self):
        return [item for item in self]






if __name__ == "__main__":
    sk = SkipList()
    print(sk)
    sk.insert(2)
    sk.insert(2)
    sk.insert(0)
    sk.insert(10)
    sk.insert(100)
    sk.insert(50)
    # sk.insert(-20)
    print(sk)
    # print(2 in sk)
    # print(100 in sk)
    # print(20 in sk)
    del sk[1]
    print(sk)
    # for item in sk: print(item)