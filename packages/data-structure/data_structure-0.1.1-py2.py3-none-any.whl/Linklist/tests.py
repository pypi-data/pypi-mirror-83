#!/usr/bin/env python
# -*- coding: utf-8 -*-


from Linklist.common import SinglyLinkedStack, SinglyLinkedQueue, \
    CircleQueue, DoublyLinkedQueue


def main():
    """Those data structures contains most common functions learnt in school"""
    a = SinglyLinkedStack()
    b = SinglyLinkedQueue()
    c = CircleQueue()
    d = DoublyLinkedQueue()

    a.push(1), a.push(2), a.push(3)
    a.pop(), a.pop()
    a.traverse()
    a.top()
    a.search(1)

    b.enqueue(1), b.enqueue(2), b.enqueue(3)
    b.traverse()
    b.dequeue()
    b.first()
    b.search(2)

    c.enqueue(1), c.enqueue(2), c.enqueue(3), c.enqueue(4)
    c.traverse()
    c.first()
    c.dequeue()
    c.search(2)

    d.enqueue_left(1)
    d.enqueue_left(2)
    d.enqueue_right(2)
    d.enqueue_right(1)
    d.traverse()
    d.first()
    d.last()
    d.dequeue_right()
    d.dequeue_left()
    d.traverse()


if __name__ == '__main__':
    main()
