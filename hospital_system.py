import sys

# ==== ADT CLASSES ====

class Patient:
    def __init__(self, id, name, age):
        self.id = id
        self.name = name
        self.age = age
        self.severity = 0

    def __str__(self):
        return f"Patient{{id={self.id}, name='{self.name}', age={self.age}, severity={self.severity}}}"


class Slot:
    def __init__(self, slotId, startTime, endTime):
        self.slotId = slotId
        self.startTime = startTime
        self.endTime = endTime
        self.booked = False
        self.next = None


class Doctor:
    def __init__(self, id, name, specialization):
        self.id = id
        self.name = name
        self.specialization = specialization
        self.headSlot = None


class Token:
    def __init__(self, tokenId, patientId, doctorId, slotId, emergency):
        self.tokenId = tokenId
        self.patientId = patientId
        self.doctorId = doctorId
        self.slotId = slotId
        self.emergency = emergency

    def __str__(self):
        return f"Token{{tokenId={self.tokenId}, patientId={self.patientId}, doctorId={self.doctorId}, slotId={self.slotId}, emergency={self.emergency}}}"


# ==== CIRCULAR QUEUE FOR ROUTINE APPOINTMENTS ====

class CircularQueue:
    def __init__(self, capacity):
        self.capacity = capacity
        self.arr = [None] * capacity
        self.front = 0
        self.rear = -1
        self.size = 0

    def isEmpty(self):
        return self.size == 0

    def isFull(self):
        return self.size == self.capacity

    def enqueue(self, token):
        if self.isFull():
            print("Routine queue is full! Cannot enqueue.")
            return
        self.rear = (self.rear + 1) % self.capacity
        self.arr[self.rear] = token
        self.size += 1

    def dequeue(self):
        if self.isEmpty():
            print("Routine queue is empty! Cannot dequeue.")
            return None
        t = self.arr[self.front]
        self.arr[self.front] = None
        self.front = (self.front + 1) % self.capacity
        self.size -= 1
        return t

    def peek(self):
        return None if self.isEmpty() else self.arr[self.front]


# ==== MIN HEAP FOR EMERGENCY TRIAGE ====

class TriageNode:
    def __init__(self, patientId, severity):
        self.patientId = patientId
        self.severity = severity


class MinHeap:
    def __init__(self, capacity):
        self.capacity = capacity
        self.heap = [None] * capacity
        self.size = 0

    def isEmpty(self):
        return self.size == 0

    def insert(self, patientId, severity):
        if self.size == self.capacity:
            print("Emergency heap full! Cannot insert.")
            return

        node = TriageNode(patientId, severity)
        self.heap[self.size] = node
        i = self.size
        self.size += 1

        while i > 0:
            parent = (i - 1) // 2
            if self.heap[parent].severity <= self.heap[i].severity:
                break
            self.heap[parent], self.heap[i] = self.heap[i], self.heap[parent]
            i = parent

    def extractMin(self):
        if self.size == 0:
            print("No emergency patients.")
            return None

        root = self.heap[0]
        self.heap[0] = self.heap[self.size - 1]
        self.heap[self.size - 1] = None
        self.size -= 1
        self.heapifyDown(0)
        return root

    def heapifyDown(self, i):
        while True:
            left = 2 * i + 1
            right = 2 * i + 2
            smallest = i

            if left < self.size and self.heap[left].severity < self.heap[smallest].severity:
                smallest = left
            if right < self.size and self.heap[right].severity < self.heap[smallest].severity:
                smallest = right

            if smallest != i:
                self.heap[smallest], self.heap[i] = self.heap[i], self.heap[smallest]
                i = smallest
            else:
                break


# ==== HASH TABLE FOR PATIENTS (CHAINING) ====

class PatientNode:
    def __init__(self, patient):
        self.patient = patient
        self.next = None


class PatientHashTable:
    def __init__(self, capacity):
        self.capacity = capacity
        self.table = [None] * capacity

    def hash(self, id):
        return abs(id) % self.capacity

    def upsert(self, patient):
        idx = self.hash(patient.id)
        curr = self.table[idx]

        while curr:
            if curr.patient.id == patient.id:
                curr.patient = patient
                return
            curr = curr.next

        newNode = PatientNode(patient)
        newNode.next = self.table[idx]
        self.table[idx] = newNode

    def get(self, id):
        idx = self.hash(id)
        curr = self.table[idx]
        while curr:
            if curr.patient.id == id:
                return curr.patient
            curr = curr.next
        return None


# ==== STACK FOR UNDO ====

class UndoAction:
    def __init__(self, type, token):
        self.type = type
        self.token = token


class UndoStack:
    def __init__(self, capacity):
        self.arr = [None] * capacity
        self.top = -1

    def push(self, action):
        if self.top == len(self.arr) - 1:
            print("Undo stack full. Cannot record action.")
            return
        self.top += 1
        self.arr[self.top] = action

    def pop(self):
        if self.top == -1:
            print("Nothing to undo.")
            return None
        t = self.arr[self.top]
        self.top -= 1
        return t


# ==== GLOBALS ====
doctors = []
routineQueue = CircularQueue(50)
emergencyHeap = MinHeap(50)
patientIndex = PatientHashTable(53)
undoStack = UndoStack(100)
globalTokenId = 1


# ==== SCHEDULE FUNCTIONS ====

def findDoctorById(id):
    for d in doctors:
        if d.id == id:
            return d
    return None


def scheduleAddSlot(doctorId, slotId, start, end):
    d = findDoctorById(doctorId)
    if d is None:
        print("Doctor not found.")
        return

    slot = Slot(slotId, start, end)
    slot.next = d.headSlot
    d.headSlot = slot
    print(f"Slot added for Doctor {d.name}")


def scheduleCancelSlot(doctorId, slotId):
    d = findDoctorById(doctorId)
    if d is None:
        print("Doctor not found.")
        return

    curr = d.headSlot
    prev = None

    while curr and curr.slotId != slotId:
        prev = curr
        curr = curr.next

    if curr is None:
        print("Slot not found.")
        return

    if prev is None:
        d.headSlot = curr.next
    else:
        prev.next = curr.next

    print(f"Slot {slotId} cancelled for Doctor {d.name}")


def findNextFreeSlot(d):
    curr = d.headSlot
    while curr:
        if not curr.booked:
            return curr
        curr = curr.next
    return None


# ==== PATIENT & BOOKING FUNCTIONS ====

def registerPatient():
    id = int(input("Enter patient id: "))
    name = input("Enter patient name: ")
    age = int(input("Enter patient age: "))

    p = Patient(id, name, age)
    patientIndex.upsert(p)
    print("Patient registered/updated:", p)


def addDoctor():
    id = int(input("Enter doctor id: "))
    name = input("Enter doctor name: ")
    spec = input("Enter specialization: ")

    d = Doctor(id, name, spec)
    doctors.append(d)
    print(f"Doctor added: {d.name}")


def bookRoutine():
    global globalTokenId

    pid = int(input("Enter patient id: "))
    p = patientIndex.get(pid)

    if p is None:
        print("Patient not found. Please register first.")
        return

    did = int(input("Enter doctor id: "))
    d = findDoctorById(did)

    if d is None:
        print("Doctor not found.")
        return

    slot = findNextFreeSlot(d)
    if slot is None:
        print("No free slots for this doctor.")
        return

    slot.booked = True
    t = Token(globalTokenId, pid, did, slot.slotId, False)
    globalTokenId += 1

    routineQueue.enqueue(t)
    undoStack.push(UndoAction("BOOK", t))

    print("Routine appointment booked:", t)


def emergencyIn():
    global globalTokenId

    pid = int(input("Enter patient id: "))
    p = patientIndex.get(pid)

    if p is None:
        print("Patient not found. Please register first.")
        return

    severity = int(input("Enter severity score (lower = more serious): "))
    p.severity = severity

    emergencyHeap.insert(pid, severity)

    t = Token(globalTokenId, pid, -1, -1, True)
    globalTokenId += 1
    undoStack.push(UndoAction("EMERGENCY", t))

    print("Emergency patient sent to triage:", p.name)


def serveNext():
    global globalTokenId

    if not emergencyHeap.isEmpty():
        node = emergencyHeap.extractMin()
        p = patientIndex.get(node.patientId)
        print("Serving EMERGENCY patient:", p)

        t = Token(globalTokenId, p.id, -1, -1, True)
        globalTokenId += 1
        undoStack.push(UndoAction("SERVE", t))
        return

    t = routineQueue.dequeue()
    if t is None:
        return

    p = patientIndex.get(t.patientId)
    d = findDoctorById(t.doctorId)

    print(f"Serving ROUTINE patient: {p.name} with Doctor {d.name if d else 'N/A'}")
    undoStack.push(UndoAction("SERVE", t))


def undoLast():
    action = undoStack.pop()
    if action is None:
        return

    print(f"Undoing last action: {action.type} for patient {action.token.patientId}")
    # Full rollback logic can be implemented


def printDoctorSummary():
    print("---- Doctor-wise Pending Summary ----")
    for d in doctors:
        pending = 0
        nextFree = None
        curr = d.headSlot

        while curr:
            if curr.booked:
                pending += 1
            if not curr.booked and nextFree is None:
                nextFree = curr
            curr = curr.next

        print(f"Doctor: {d.name} (ID {d.id})")
        print(f"  Pending slots (booked): {pending}")
        if nextFree:
            print(f"  Next free slot: {nextFree.slotId} [{nextFree.startTime} - {nextFree.endTime}]")
        else:
            print("  No free slots available.")


# ==== MENU ====

def mainMenu():
    while True:
        print("\n===== Hospital Appointment & Triage System =====")
        print("1. Register / Update Patient")
        print("2. Add Doctor")
        print("3. Add Slot for Doctor")
        print("4. Book Routine Appointment")
        print("5. Emergency In (Triage)")
        print("6. Serve Next Patient")
        print("7. Undo Last Action")
        print("8. Doctor-wise Pending Report")
        print("9. Exit")

        ch = int(input("Enter choice: "))

        if ch == 1:
            registerPatient()
        elif ch == 2:
            addDoctor()
        elif ch == 3:
            did = int(input("Enter doctor id: "))
            sid = int(input("Enter slot id: "))
            st = input("Enter start time (e.g. 10:00): ")
            et = input("Enter end time (e.g. 10:15): ")
            scheduleAddSlot(did, sid, st, et)
        elif ch == 4:
            bookRoutine()
        elif ch == 5:
            emergencyIn()
        elif ch == 6:
            serveNext()
        elif ch == 7:
            undoLast()
        elif ch == 8:
            printDoctorSummary()
        elif ch == 9:
            print("Exiting...")
            sys.exit(0)
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    mainMenu()
