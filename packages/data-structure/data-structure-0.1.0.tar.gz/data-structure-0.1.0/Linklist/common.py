#!/usr/bin/env python
# -*- coding: utf-8 -*-


class SinglyNode(object):
    """Restrict attributes for this data structure"""
    __slots__ = 'data', 'link'

    def __init__(self, data, link):
        """Public"""
        self.data = data
        self.link = link


class DoublyNode(object):
    """Restrict attributes for this data structure"""
    __slots__ = 'data', 'prev', 'link'

    def __init__(self, data, prev, link):
        """Public"""
        self.data = data
        self.prev = prev
        self.link = link


"""Singly link list is a collection of nodes that collectively form a linear sequence."""


class SinglyLinkList(object):

    def __init__(self):
        """Public"""
        self._head = SinglyNode(None, None)
        self._size = 0

    def __len__(self):
        return self._size

    def _is_empty(self):
        return self._size == 0

    def _insert(self, e, cursor):
        element = SinglyNode(e, None)
        element.link = cursor.link
        cursor.link = element
        self._size += 1
        print(element.data)
        return element.data

    def _delete(self, node):
        if self._is_empty():
            raise EmptyError
        self._head.link = node.link
        print(node.data)
        node.data = node.link = None
        self._size -= 1

    def _traverse(self):
        linklist = []
        if self._is_empty():
            raise EmptyError
        current = self._head
        while current.link:
            linklist.append(current.link.data)
            current = current.link
        print(linklist, self._size)
        return linklist

    def _search(self, e):
        """Find a specific element"""
        result = []
        if self._is_empty():
            raise EmptyError
        cursor = self._head
        while cursor.link:
            if cursor.link.data == e:
                result.append((cursor.link, cursor.link.data))
            cursor = cursor.link
        print(result)
        return result


"""A doubly linked list can provide greater symmetry, each node keeps 
an explicit reference to the node before it and a reference to the node after it."""


class DoublyLinkList(object):
    """Restrict attributes for this data structure"""
    __slots__ = 'head', 'tail', 'size'

    def __init__(self):
        self.head = DoublyNode(None, None, None)
        self.tail = DoublyNode(None, None, None)
        self.head.link = self.tail
        self.tail.prev = self.head
        self.size = 0

    def __len__(self):
        return self.size

    def _is_empty(self):
        return self.size == 0

    def _insert(self, e, predecessor, successor):
        element = DoublyNode(e, predecessor, successor)
        predecessor.link = element
        successor.prev = element
        self.size += 1
        return element.data

    def _delete(self, node):
        if self._is_empty():
            raise EmptyError
        predecessor = node.prev
        successor = node.link
        predecessor.link = successor
        successor.prev = predecessor
        self.size -= 1
        e = node.data
        node.prev = node.link = node.data = None
        return e

    def traverse(self):
        queue = []
        if self._is_empty():
            raise EmptyError
        current = self.head.link
        while current != self.tail:
            queue.append(current.data)
            current = current.link
        print(queue, self.size)
        return queue


class SinglyLinkedStack(SinglyLinkList):

    def push(self, e):
        if e is None:
            raise EmptyError
        self._insert(e, self._head)

    def pop(self):
        if self._is_empty():
            raise EmptyError
        self._delete(self._head.link)

    def top(self):
        if self._is_empty():
            raise EmptyError
        print(self._head.link.data)
        return self._head.link.data

    def traverse(self):
        """Traverse from top to bottom of the stack, Then show it in a list"""
        return self._traverse()

    def search(self, e):
        """Find a specific element"""
        return self._search(e)


class SinglyLinkedQueue(SinglyLinkList):

    def __init__(self):
        # self._head = SinglyNode(None, None)
        # self._size = 0
        super().__init__()
        self._tail = SinglyNode(None, None)

    def enqueue(self, e):
        if e is None:
            raise EmptyError
        element = SinglyNode(e, None)
        if self._is_empty():
            self._head.link = element
        else:
            self._tail.link = element
        self._tail = element
        self._size += 1
        print(element.data)
        return element.data

    def dequeue(self):
        if self._is_empty():
            raise EmptyError
        else:
            element = self._head.link.data
            self._head = self._head.link
            self._size -= 1
            if self._is_empty():
                self._tail = None
        print(element)
        return element

    def traverse(self):
        return self._traverse()

    def first(self):
        if self._is_empty():
            raise EmptyError
        print(self._head.link.data)

    def search(self, e):
        return self._search(e)


class DoublyLinkedQueue(DoublyLinkList):

    def first(self):
        if self._is_empty():
            raise EmptyError
        print(self.head.link.data)
        return self.head.link.data

    def last(self):
        if self._is_empty():
            raise EmptyError
        print(self.tail.prev.data)
        return self.tail.prev.data

    def enqueue_left(self, e):
        if e is None:
            raise EmptyError
        self._insert(e, self.head, self.head.link)

    def enqueue_right(self, e):
        if e is None:
            raise EmptyError
        self._insert(e, self.tail.prev, self.tail)

    def dequeue_left(self):
        if self._is_empty():
            raise EmptyError
        return self._delete(self.head.link)

    def dequeue_right(self):
        if self._is_empty():
            raise EmptyError
        return self._delete(self.tail.prev)


class CircleQueue(object):

    def __init__(self):
        self._tail = None
        self._size = 0

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    def enqueue(self, e):
        if e is None:
            raise EmptyError
        element = SinglyNode(e, None)
        if self.is_empty():
            element.link = element
        else:
            element.link = self._tail.link
            self._tail.link = element
        self._tail = element
        self._size += 1
        return element.data

    def dequeue(self):
        if self.is_empty():
            raise EmptyError
        element = self._tail.link
        if self._size == 1:
            self._tail = None
        else:
            self._tail.link = element.link
        self._size -= 1
        return element.data

    def traverse(self):
        queue = []
        if self.is_empty():
            raise EmptyError
        current = self._tail.link
        queue.append(current.data)
        while current != self._tail:
            current = current.link
            queue.append(current.data)
        print(queue, self._size)
        return queue

    def first(self):
        if self.is_empty():
            raise EmptyError
        first = self._tail.link
        print(first.data)
        return first.data

    def search(self, e):
        if e in self.traverse():
            return True
        else:
            return False


'''Exceptions' definition of your own make'''


class EmptyError(Exception):

    def __str__(self):
        return u'This object is empty.'
