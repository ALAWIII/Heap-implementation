
class HeapQueue:
    def __init__(self, data: list = [], max_priority: bool = False):
        """data parameter for accepting list with values that need to be treated as a heap rather than (inserting
        each value alone which requires O(nlog(n).) but when giving the whole list it will construct the heap in O(n/2)
        which is better using _buildHeap() method.
        """
        self._data = data
        self.max_priority = max_priority
        if len(self._data) > 0:
            self._buildHeap()

    def __len__(self):
        return len(self._data)

    def is_empty(self):
        """check if the heap is empty"""
        return len(self) == 0

    def _parent(self, childIndex):
        """return the parent location of the child location"""
        return (childIndex - 1) // 2

    def _left(self, parentIndex):
        """return the left location of the parent location"""
        return 2 * parentIndex + 1

    def _right(self, parentIndex):
        """return the right location of the parent location"""
        return 2 * parentIndex + 2

    def _has_left(self, parentIndex):
        """check whether the parent has a left child"""
        return self._left(parentIndex) < len(self)

    def _has_right(self, parentIndex):
        """check whether the parent has a right child"""
        return self._right(parentIndex) < len(self)

    def _swap(self, indexA, indexB):
        """swap the values that are stored in a given indexes"""
        self._data[indexA], self._data[indexB] = self._data[indexB], self._data[indexA]

    def _first_higher_priority(self, valueA, valueB):
        """this method will be called by other methods!
        if the heap was specified to be max_heap then
            check if the valueA > valueB
        if the heap was specified to be min_heap then check valueA < valueB
        """
        return valueA > valueB if self.max_priority else valueA < valueB

    def _higherpriority(self, indexA, indexB):
        """checks whether the one of the indexes has the higher priority and will return it"""
        if indexA >= len(self):
            return indexB
        valueA = self._data[indexA]
        valueB = self._data[indexB]
        isFirst = self._first_higher_priority(valueA, valueB)
        return indexA if isFirst else indexB

    def _upHeap(self, index):
        """it will iterate over the heap values using child and parent indexes and will swap the values depending
        upon the priority"""
        child = index
        parent = self._parent(child)
        while child > 0 and child == self._higherpriority(child, parent):
            self._swap(child, parent)
            child = parent
            parent = self._parent(child)

    def _downHeap(self, index):
        """it will iterate down from index to len(heap)-1 ,the parent will check whether the left or the right
        children have the higher priority so its going to swap the values"""
        parent = index
        while True:
            left = self._left(parent)
            right = self._right(parent)
            chosen = self._higherpriority(left, parent)  # will the higher priority
            chosen = self._higherpriority(right, chosen)
            if chosen == parent:
                return  # if the chosen is the parent then the parent is in the right place and exit the method
            self._swap(parent, chosen)
            parent = chosen

    def add(self, value):
        """it will add new value to the end of the list then we will call upheap to move the value from len(heap) to
        the right place"""
        self._data.append(value)
        self._upHeap(len(self) - 1)

    def remove_peak(self):
        """it will swap the value at the 0 index with the value at the len(self._data)-1 index then pop it out of the
        list ,and then will call the downheap to move the value at 0 index to the right place
        """
        if self.is_empty():
            return

        self._swap(0, len(self) - 1)
        value = self._data.pop()
        self._downHeap(0)
        return value

    def removeAt(self, index):
        """removing the value at given index!
        it will swap the value at the index given with the last one and then pop it out of the list
        then calling downheap and upheap to set the values at the right place"""
        if index < 0 or index >= len(self):
            return

        self._swap(index, len(self) - 1)
        value = self._data.pop()
        self._downHeap(index)
        self._upHeap(len(self) - 1)
        return value

    def peak(self):
        """return the value at the 0 index"""
        if self.is_empty():
            return
        return self._data[0]

    def index_of(self, key, index=0):
        """return the index of the given key at a given index ,it works recursively,
        if the left returns -1 then search at the right"""

        if index >= len(self):
            return -1
        if self._first_higher_priority(key, self._data[index]):
            return -1
        if key == self._data[index]:
            return index
        left = self.index_of(key, self._left(index))
        return left if left != -1 else self.index_of(key, self._right(index))

    def _buildHeap(self):
        """it will build the heap be taking the array given in the data parameter when initializing the heap object"""
        if self.is_empty():
            return
        middle = len(self._data) // 2 - 1
        for i in range(middle, -1, -1):
            self._downHeap(i)

    def __str__(self):
        return f"{self._data}"

    def _sort_checker(self, left_right, chosen, down_sort=True):
        if down_sort:
            return self._data[left_right] > self._data[chosen]
        return self._data[left_right] < self._data[chosen]

    def _sort_up_down(self, start, end, down_sort=True):
        parent = start
        while True:
            left = self._left(parent)
            right = self._right(parent)
            chosen = parent
            if left < end and self._sort_checker(left, chosen, down_sort):
                chosen = left
            if right < end and self._sort_checker(right, chosen, down_sort):
                chosen = right
            if chosen == parent:
                return
            self._swap(parent, chosen)
            parent = chosen

    def _func(self, _sort_up_down, down_sort=True):
        # convert min heap to max heap or vice versa,swapping reside every element to its right place
        middle = len(self) // 2 - 1
        for i in range(middle, -1, -1):
            _sort_up_down(i, len(self), down_sort)

    def _func2(self, _sort_up_down, down_sort=True):
        """it will do n/2 swaps and (up or down) heap to place the elements in their right place"""
        for i in range(len(self) - 1, -1, -1):
            self._swap(0, i)
            _sort_up_down(0, i, down_sort)

    def sort(self, ascending=True):
        """the point is to sort based on your needs it has to do some conversions from min to max or from max to min
        or no conversions at all!

        if it was a min_heap and you want  ascending you run condition 2,4,
        if it was a min_heap and you want descending you run condition 3,
        if it was a max_heap and you want ascending you have you run condition 4
        if it was a max_heap and you want descending you run condition 1,3"""

        if not ascending and self.max_priority:  # condition 1 , to convert to min_heap
            self.max_priority = False
        elif ascending and not self.max_priority:  # condition 2 , to convert to max_heap
            self.max_priority = True

        if not self.max_priority:  # condition 3
            # for the up_sort
            self._func(self._sort_up_down, down_sort=False)
            self._func2(self._sort_up_down, down_sort=False)
        else:  # condition 4
            # for the down_sort
            self._func(self._sort_up_down)
            self._func2(self._sort_up_down)



# Examples
obj = HeapQueue(data=[1, 2, 3, 4, 5, 6, 7, 8, 9], max_priority=True)
obj.sort(ascending=True)

obj2 = HeapQueue(data=[1, 2, 3, 4, 5, 6, 7, 8, 9], max_priority=True)
obj2.sort(ascending=False)

obj3 = HeapQueue(data=[1, 2, 3, 4, 5, 6, 7, 8, 9], max_priority=False)
obj3.sort(ascending=True)

obj4 = HeapQueue(data=[1, 2, 3, 4, 5, 6, 7, 8, 9], max_priority=False)
obj4.sort(ascending=False)

print(obj)
print(obj2)
print(obj3)
print(obj2)
