from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Patient:
    """
    Patient model shared by baseline and optimized systems.
    """
    id: int
    name: str
    severity: int      # 1 (low) to 5 (critical)
    arrival_time: int  # increasing counter or timestamp


class _Node:
    def __init__(self, data: Patient) -> None:
        self.data: Patient = data
        self.next_ptr: Optional["_Node"] = None
        self.prev_ptr: Optional["_Node"] = None


class FCFSTriageSystem:
    """
    First-Come-First-Serve triage system using a doubly linked list queue.
    """

    def __init__(self, max_capacity: Optional[int] = None) -> None:
        self.head: Optional[_Node] = None
        self.tail: Optional[_Node] = None
        self._size: int = 0
        self._capacity: Optional[int] = max_capacity

    def is_full(self) -> bool:
        return self._capacity is not None and self._size >= self._capacity

    def is_empty(self) -> bool:
        return self._size == 0

    def arrive(self, patient: Patient) -> bool:
        if self.is_full():
            return False

        new_node = _Node(patient)

        if self.head is None:
            self.head = self.tail = new_node
        else:
            assert self.tail is not None
            self.tail.next_ptr = new_node
            new_node.prev_ptr = self.tail
            self.tail = new_node

        self._size += 1
        return True

    def serve_next(self) -> Optional[Patient]:
        if self.head is None:
            return None

        node = self.head
        self.head = node.next_ptr

        if self.head is not None:
            self.head.prev_ptr = None
        else:
            self.tail = None

        self._size -= 1
        return node.data

    def __len__(self) -> int:
        return self._size

    def traverse_forward(self) -> List[Patient]:
        result: List[Patient] = []
        current = self.head
        while current is not None:
            result.append(current.data)
            current = current.next_ptr
        return result

    def traverse_backward(self) -> List[Patient]:
        result: List[Patient] = []
        current = self.tail
        while current is not None:
            result.append(current.data)
            current = current.prev_ptr
        return result

    def display(self) -> None:
        if self.is_empty():
            print("\nQueue is empty!")
            return

        print("\nQueue elements (front to rear):")
        current = self.head
        while current is not None:
            p = current.data
            print(f"  id={p.id}, name={p.name}, severity={p.severity}")
            current = current.next_ptr

    def get_current_size(self) -> int:
        return self._size

    def get_max_size(self) -> Optional[int]:
        return self._capacity


def clear_screen() -> None:
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def print_section(title: str) -> None:
    print("\n" + "-"*60)
    print(f"  {title}")
    print("-"*60)


def print_success(msg: str) -> None:
    print(f"[OK] {msg}")


def print_error(msg: str) -> None:
    print(f"[ERROR] {msg}")


def read_int(prompt: str, min_val: Optional[int] = None,
             max_val: Optional[int] = None) -> int:
    while True:
        raw = input(f"  > {prompt}").strip()
        if not raw:
            print_error("Input cannot be empty.")
            continue
        try:
            value = int(raw)
        except ValueError:
            print_error(f"Invalid input. Please enter a valid number.")
            continue

        if min_val is not None and value < min_val:
            print_error(f"Value too low. Please enter at least {min_val}.")
            continue
        if max_val is not None and value > max_val:
            print_error(f"Value too high. Please enter at most {max_val}.")
            continue

        return value


def read_non_empty(prompt: str) -> str:
    while True:
        s = input(f"  > {prompt}").strip()
        if s:
            return s
        print_error("Input cannot be empty. Please try again.")


if __name__ == "__main__":
    clear_screen()
    print("\n" + "="*60)
    print("  FCFS TRIAGE SYSTEM (BASELINE)")
    print("  First-Come-First-Serve Queue Implementation")
    print("="*60 + "\n")

    arrival_counter = 0
    option = 0

    queue_size = read_int("Enter queue max capacity (e.g. 5 or 10): ", 1)
    system = FCFSTriageSystem(queue_size)
    print_success(f"System initialized with capacity: {queue_size}\n")

    while option != 9:
        print("\n" + "="*60)
        print("  MAIN MENU - What would you like to do?")
        print("="*60)
        print(" 1. Add patient to queue")
        print(" 2. Serve next patient (FIFO order)")
        print(" 3. View front patient in queue")
        print(" 4. View rear patient in queue")
        print(" 5. Check if queue is FULL")
        print(" 6. Check if queue is EMPTY")
        print(" 7. Display entire queue")
        print(" 8. View queue statistics")
        print(" 9. Exit program")
        print("="*60)
        option = read_int("Enter your choice (1-9): ", 1, 9)

        if option == 1:
            print_section("ADD NEW PATIENT")
            name = read_non_empty("Patient name: ")
            pid = read_int("Patient ID: ")
            severity = read_int("Severity level (1=Low to 5=Critical): ", 1, 5)
            arrival_counter += 1

            p = Patient(
                id=pid,
                name=name,
                severity=severity,
                arrival_time=arrival_counter,
            )
            if system.arrive(p):
                print_success(f"Patient '{name}' (ID: {pid}) added to queue successfully!")
            else:
                print_error("Failed to add patient - queue is at full capacity!")

        elif option == 2:
            print_section("SERVE NEXT PATIENT")
            p = system.serve_next()
            if p is not None:
                print_success(f"Now serving: {p.name}")
                print(f"  Patient ID:    {p.id}")
                print(f"  Severity:      {p.severity}/5")
                print(f"  Arrival Order: Patient #{p.arrival_time}")
            else:
                print_error("Cannot serve - queue is empty!")

        elif option == 3:
            print_section("FRONT PATIENT (Next to be served)")
            if system.is_empty():
                print_error("Queue is empty!")
            else:
                front_patient = system.traverse_forward()[0]
                print(f"  Name:           {front_patient.name}")
                print(f"  ID:             {front_patient.id}")
                print(f"  Severity:       {front_patient.severity}/5")
                print(f"  Arrival Order:  Patient #{front_patient.arrival_time}")

        elif option == 4:
            print_section("REAR PATIENT (Last in queue)")
            if system.is_empty():
                print_error("Queue is empty!")
            else:
                rear_patient = system.traverse_backward()[0]
                print(f"  Name:           {rear_patient.name}")
                print(f"  ID:             {rear_patient.id}")
                print(f"  Severity:       {rear_patient.severity}/5")
                print(f"  Arrival Order:  Patient #{rear_patient.arrival_time}")

        elif option == 5:
            print_section("QUEUE CAPACITY STATUS")
            size = system.get_current_size()
            cap = system.get_max_size()
            cap_str = str(cap) if cap is not None else "Unlimited"
            usage = (size / cap * 100) if cap is not None else 0
            
            if system.is_full():
                print_error(f"Queue is FULL! {size}/{cap_str} patients")
            else:
                print_success(f"Queue is NOT full. {size}/{cap_str} patients")
            
            print(f"  Current size:   {size}")
            print(f"  Max capacity:   {cap_str}")
            if cap is not None:
                print(f"  Usage percent:  {usage:.1f}%")

        elif option == 6:
            print_section("QUEUE EMPTY CHECK")
            size = system.get_current_size()
            
            if system.is_empty():
                print_error("Queue is EMPTY! No patients waiting.")
            else:
                print_success(f"Queue is NOT empty. {size} patient(s) waiting.")
            
            print(f"  Total patients: {size}")

        elif option == 7:
            print_section("DISPLAY ALL PATIENTS (Front to Rear)")
            if system.is_empty():
                print_error("Queue is empty! No patients to display.")
            else:
                patients = system.traverse_forward()
                print("\n  " + "-"*110)
                print(f"  {'#':<4} | {'Name':<20} | {'ID':<5} | {'Severity':<10} | {'Arrival Order':<15}")
                print("  " + "-"*110)
                for i, p in enumerate(patients, 1):
                    severity_display = "[" + "*" * p.severity + " " * (5 - p.severity) + "]"
                    print(f"  {i:<4} | {p.name:<20} | {p.id:<5} | {severity_display:<10} | Patient #{p.arrival_time:<11}")
                print("  " + "-"*110)
                print(f"\n  Total patients in queue: {len(patients)}")

        elif option == 8:
            print_section("QUEUE STATISTICS")
            size = system.get_current_size()
            cap = system.get_max_size()
            cap_str = str(cap) if cap is not None else "Unlimited"
            patients = system.traverse_forward()
            
            print(f"\n  CAPACITY INFORMATION:")
            print(f"    Total patients:  {size}")
            print(f"    Max capacity:    {cap_str}")
            
            if patients:
                avg_severity = sum(p.severity for p in patients) / len(patients)
                max_severity = max(p.severity for p in patients)
                min_severity = min(p.severity for p in patients)
                
                print(f"\n  SEVERITY STATISTICS:")
                print(f"    Average severity: {avg_severity:.1f}/5")
                print(f"    Max severity:     {max_severity}/5")
                print(f"    Min severity:     {min_severity}/5")
            else:
                print_error("No patients in queue for statistics.")

        elif option == 9:
            print_section("EXITING FCFS TRIAGE SYSTEM")
            print("  Thank you for using the system!")
            print("  Goodbye.")
            break
