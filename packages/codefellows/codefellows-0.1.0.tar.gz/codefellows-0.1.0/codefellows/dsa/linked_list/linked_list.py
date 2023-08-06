""""
LinkedList & Node Implementations
Covers classes 5,6 and 7
"""


class LinkedList:
    """
    Singly Linked List
    """

    def __init__(self, head=None, values=None):
        self.head = head

        if values:
            for value in reversed(values):
                self.insert(value)

    def insert(self, value):
        """
        Adds value to beginning (aka head) of list
        """
        self.head = Node(value, self.head)

    def includes(self, value):
        """
        returns True/False if value found in list
        """

        current = self.head

        while current:

            if current.value == value:
                return True

            current = current.next

        return False

    def __str__(self):
        """returns linked list in stringy form

        Returns:
            [string] -- e.g. ['apples'],['bananas'],
        """
        output = ""

        current = self.head

        while current:
            output += f"[{current.value}],"
            current = current.next

        return output

    def append(self, value):
        """"adds value to end of list"""

        node = Node(value)

        if not self.head:
            self.head = node
            return

        current = self.head

        while current.next:
            current = current.next

        current.next = node

    def insert_before(self, value, new_value):
        """"inserts new_value before the given value"""

        current = self.head

        while current and current.next:
            if current.next.value == value:
                node = Node(new_value, current.next)
                current.next = node
                return

            current = current.next

        raise TargetError(f"{value} not in list")

    def insert_after(self, value, new_value):
        """"inserts new_value before the given value"""

        current = self.head

        while current:
            if current.value == value:
                node = Node(new_value, current.next)
                current.next = node
                return

            current = current.next

        raise TargetError(f"{value} not in list")

    def kth_from_end(self, k):
        """returns the item k back from end"""

        leader = self.head

        follower = None

        paces_behind = 0

        while leader:

            leader = leader.next

            if follower:
                follower = follower.next
            elif paces_behind == k:
                follower = self.head
            else:
                paces_behind += 1

        if not follower:
            raise TargetError("k is out of range")

        return follower.value


class Node:
    """
    Node for use in a Linked List
    """

    def __init__(self, value, next_=None):
        self.value = value
        self.next = next_


class TargetError(ValueError):
    pass
