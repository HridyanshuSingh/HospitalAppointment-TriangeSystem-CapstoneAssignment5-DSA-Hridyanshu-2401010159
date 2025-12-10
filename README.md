# 🚑 Hospital Appointment & Triage System
A Python-Based Simulation Using Core Data Structures


📘 Overview

The Hospital Appointment & Triage System is a Python-based console application that simulates how hospitals manage:

Patient registrations

Doctor scheduling

Routine appointments

Emergency triage

Undo actions

Doctor-wise reporting

The project demonstrates how various fundamental data structures work together in a real-world scenario.

🧠 Tech Stack & Concepts Used
Feature	Data Structure	Purpose
Patient Management	Hash Table (Chaining)	O(1) lookup & insert
Routine Appointment Queue	Circular Queue	FIFO scheduling
Emergency Triage	Min Heap	Priority handling based on severity
Doctor Time Slots	Singly Linked List	Fast insertion & traversal
Undo Operations	Stack	LIFO operation reversal
🎯 Key Features
✔ 1. Patient Registration

Stores/updates patient details with constant time lookup.

✔ 2. Doctor Management

Store doctors and dynamically manage their available time slots.

✔ 3. Appointment System

Books routine appointments using queue

Finds next free slot automatically

Generates tokens

✔ 4. Emergency Handling

Emergency patients added to Min Heap

Highest priority patient (lowest score) served first

✔ 5. Serve Next

Emergency > Routine

Fully automated workflow

✔ 6. Undo Last Action

Uses a stack to maintain operation history.

✔ 7. Detailed Reports

Doctor-wise summary including next free slot and pending load.

🏗 System Architecture
+-------------------+
|   Patient Index   |  --> HashTable (Chaining)
+-------------------+

+-------------------+
| Doctors & Slots   |  --> Linked List
+-------------------+

+-------------------+
| Routine Queue     |  --> Circular Queue
+-------------------+

+-------------------+
| Emergency Triage  |  --> Min Heap
+-------------------+

+-------------------+
| Undo Operations   |  --> Stack
+-------------------+

📂 Project Structure
HospitalSystem/
│
├── hospital_system.py   # Main program
├── README.md            # Documentation
└── samples/             # (Optional) Sample outputs or screenshots

⚙️ Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/<your-username>/Hospital-System.git
cd Hospital-System

2️⃣ Run the Program
python hospital_system.py

▶️ Usage

The menu-driven interface provides:

===== Hospital Appointment & Triage System =====
1. Register / Update Patient
2. Add Doctor
3. Add Slot for Doctor
4. Book Routine Appointment
5. Emergency In (Triage)
6. Serve Next Patient
7. Undo Last Action
8. Doctor-wise Pending Report
9. Exit

Choose options by entering corresponding numbers.

📊 Time & Space Complexity
Operation	Time Complexity	Space
Queue enqueue/dequeue	O(1)	O(n)
Heap insert/extract-min	O(log n)	O(n)
HashTable insert/search	O(1) avg	O(n)
Stack push/pop	O(1)	O(n)
Linked List insert	O(1)	O(n)
Find next free slot	O(k)	O(k)
