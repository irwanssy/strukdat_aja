class Node:
    def __init__(self, data):
        self.data = data   
        self.next = None  
class Queue:
    def __init__(self):
        self.front = None
        self.rear = None
        self._size = 0

    def enqueue(self, kendaraan):
        new_node = Node(kendaraan)
        if self.rear is None:
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node
        self._size += 1

    def dequeue(self):
        if self.front is None:
            return None
        temp = self.front
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        self._size -= 1
        return temp.data

    def size(self):
        return self._size


    def display(self):
        result = []
        current = self.front
        while current:
            result.append(current.data)
            current = current.next
        return result

class MultiQueueTol:

    def __init__(self):
        self.tol1 = Queue()
        self.tol2 = Queue()
        self.tol3 = Queue()

    #Ini itu untuk kendaraan masuk
    def masuk_tol(self, kendaraan):
        if self.tol1.size() <= self.tol2.size() and self.tol1.size() <= self.tol3.size():
            self.tol1.enqueue(kendaraan)
            return 1
        elif self.tol2.size() <= self.tol1.size() and self.tol2.size() <= self.tol3.size():
            self.tol2.enqueue(kendaraan)
            return 2
        else:
            self.tol3.enqueue(kendaraan)
            return 3

    def keluar_tol(self, nomor_tol):
        if nomor_tol == 1:
            return self.tol1.dequeue()
        elif nomor_tol == 2:
            return self.tol2.dequeue()
        elif nomor_tol == 3:
            return self.tol3.dequeue()


    def lihat_antrian(self):
        return {
            "Tol 1": self.tol1.display(),
            "Tol 2": self.tol2.display(),
            "Tol 3": self.tol3.display()
        }