import os
from typing import Dict


class Node:
    def __init__(self, key: str, value) -> None:
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

    def to_string(self):
       result = ""
       if self.prev:
           result += str(self.prev.value)

       result += f" < {self.value} > "

       if self.next:
           result += str(self.next.value)
       return result


class DoublyLinkedList:
    def __init__(self) -> None:
        self.head: Node = None
        self.tail: Node = None
        self.size = 0

    def add(self, node: Node):
        if not self.head:
            node.prev = None
            node.next = None
            self.head = node
            self.tail = node
            self.size = 1
        else:
            self.tail.next = node
            node.prev = self.tail
            node.next = None
            self.tail = self.tail.next
            self.size += 1

    def remove(self , node : Node):
        print(f"Removing the node {node.to_string()}")
        is_head = self.head == node
        is_tail = self.tail == node
        node_next = node.next
        node_prev = node.prev
        if is_head and is_tail:
            self.head = None
            self.tail = None
            self.size = 0
            return
        elif is_head:
            self.head = node_next
            self.head.prev = None
        elif is_tail:
            self.tail = node_prev
            self.tail.next = None
        else:
            node_prev.next = node_next
            node_next.prev = node_prev

        self.size -= 1


    def remove_head(self):
        self.remove(self.head)

    def remove_tail(self):
        self.remove(self.tail)

    def reset(self):
        self.head = None
        self.tail = None
        self.size = 0

    def to_string(self):
        current = self.head
        result = ""
        while(current):
            result += f"{current.value}"
            current = current.next
            if current:
                result += " >"
        return result


class LRUCache:
    def __init__(self, capacity: int) -> None:
        self.capacity: int = capacity
        self.cache_table: Dict[str, Node] = {}
        self.list: DoublyLinkedList = DoublyLinkedList()

    def remove_node(self , node : Node):
        key = node.key
        del self.cache_table[key]
        self.list.remove(node)

    def put(self, key: str, val):
        has_key = key in self.cache_table
        if has_key:
            self.remove_node(self.cache_table[key])

        if len(self.cache_table) == self.capacity:
            print("Reached max cache size. use remove policy")
            oldest_node : Node = self.list.head
            self.remove_node(oldest_node)
        self.save(key, val)
        self.print()

    def print(self):
        print("/////////////")
        print("Cache table is")
        table = ""
        for key, node in self.cache_table.items():
            table += f"{node.key},{node.value},"
        print(table)
        print("List is")
        print(self.list.to_string())
        print("/////////////")

    def save(self, key: str, val: str):
        new_node = Node(key , val)
        self.list.add(new_node)
        self.cache_table[key] = new_node

    def get(self, key: str):
        if key in self.cache_table:
            self.update_list(key)
            self.print()
            return self.cache_table[key].value
        else:
            print("There is no such key in the cache")
            return None

    def update_list(self, key: str):
        print("Updating the list...")
        print("Before")
        print(self.list.to_string())
        node = self.cache_table[key]
        self.list.remove(node)
        self.list.add(node)
        print("After")
        print(self.list.to_string())


def setup(cap):
    cache = LRUCache(cap)
    for index in range(1 , cap +1 ):
        cache.put(str(index),index)
    return cache

