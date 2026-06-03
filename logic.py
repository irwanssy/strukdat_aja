class Queue:

    def __init__(self):
        self.data = []

    def enqueue(self, kendaraan):
        self.data.append(kendaraan)

    def dequeue(self):
        if len(self.data) > 0:
            return self.data.pop(0)

    def size(self):
        return len(self.data)

    def display(self):
        return self.data


class MultiQueueTol:

    def __init__(self):
        self.tol1 = Queue()
        self.tol2 = Queue()
        self.tol3 = Queue()

    #Ini itu untuk kendaraan masuk
    def masuk_tol(self, kendaraan):
        if self.tol1.size() <= self.tol2.size() and self.tol1.size() <= self.tol3.size():
            self.tol1.enqueue(kendaraan)
        elif self.tol2.size() <= self.tol1.size() and self.tol2.size() <= self.tol3.size():
            self.tol2.enqueue(kendaraan)
        else:
            self.tol3.enqueue(kendaraan)

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