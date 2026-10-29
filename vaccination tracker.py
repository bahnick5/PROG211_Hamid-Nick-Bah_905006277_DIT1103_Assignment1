"""
Vaccination Tracker
PROG211 - Object-Oriented Programming 1
Assignment: Real-World Solutions under DPG Standards

Domain  : Health (Vaccination Tracker)
Concepts: Task 1 - classes, attributes, methods, object interaction
          Task 2 - one data structure (dictionary) + add/display functions
                   (a tuple is also used for the extra marks)
          Task 3 - instance, class and static methods

Digital Public Goods (DPG) design choices
  * Privacy-respecting : no names, phone numbers or addresses are stored.
                         Each person is an anonymous record ID plus an age
                         GROUP and a DISTRICT only.
  * Inclusive          : plain-text menus, clear messages, no colour or
                         special hardware needed; works in any terminal.
  * Modular / reusable : Vaccine and VaccinationRecord are independent
                         classes that can be imported into other programs.
  * Open source        : plain Python 3, standard library only, no paid
                         dependencies.
"""

from datetime import date, timedelta


# ---------------------------------------------------------------------------
# Class 1: Vaccine
# ---------------------------------------------------------------------------
class Vaccine:
    """A type of vaccine and the schedule of doses it requires."""

    # Class attribute: shared by every Vaccine object.
    total_vaccines = 0

    def __init__(self, name, doses_required, interval_days):
        self.name = name
        self.doses_required = doses_required
        self.interval_days = interval_days
        # TUPLE (immutable): days after the first dose that each dose is due.
        # e.g. 3 doses, 28 days apart -> (0, 28, 56)
        self.dose_schedule = tuple(interval_days * i for i in range(doses_required))
        Vaccine.total_vaccines += 1

    # Instance method
    def display_info(self):
        print(f"Vaccine : {self.name}")
        print(f"Doses   : {self.doses_required}")
        print(f"Schedule: day offsets {self.dose_schedule}")

    # Class method
    @classmethod
    def get_total_vaccines(cls):
        """Return how many Vaccine objects have been created."""
        return cls.total_vaccines


# ---------------------------------------------------------------------------
# Class 2: VaccinationRecord
# ---------------------------------------------------------------------------
class VaccinationRecord:
    """An anonymous vaccination record for one person.

    PRIVACY: only an anonymous ID, an age group and a district are kept.
    """

    AGE_GROUPS = ("0-5", "6-17", "18-49", "50+")

    # Class attribute: shared by every record.
    total_records = 0

    def __init__(self, record_id, age_group, district, vaccine):
        if not VaccinationRecord.is_valid_id(record_id):
            raise ValueError("Record ID must look like 'VR-001'.")
        if age_group not in VaccinationRecord.AGE_GROUPS:
            raise ValueError(f"Age group must be one of {VaccinationRecord.AGE_GROUPS}.")
        self.record_id = record_id
        self.age_group = age_group
        self.district = district
        self.vaccine = vaccine          # interaction: a record HAS a Vaccine object
        self.doses_given = []           # list of dates on which doses were given

    # ---- Instance methods -------------------------------------------------
    def give_dose(self, dose_date=None):
        """Record a dose. Refuses if the course is already complete."""
        if self.is_complete():
            print(f"  [{self.record_id}] Already fully vaccinated. No more doses needed.")
            return False
        self.doses_given.append(dose_date or date.today())
        print(f"  [{self.record_id}] Dose {len(self.doses_given)} of "
              f"{self.vaccine.doses_required} recorded.")
        return True

    def is_complete(self):
        return len(self.doses_given) >= self.vaccine.doses_required

    def next_due_date(self):
        """Return the date of the next dose, or None if complete / not started."""
        if self.is_complete() or not self.doses_given:
            return None
        offset = self.vaccine.dose_schedule[len(self.doses_given)]
        return self.doses_given[0] + timedelta(days=offset)

    def update_record(self, district=None, age_group=None):
        """Update the non-sensitive details of a record."""
        if district:
            self.district = district
        if age_group:
            if age_group not in VaccinationRecord.AGE_GROUPS:
                print(f"  Invalid age group '{age_group}'. Not changed.")
            else:
                self.age_group = age_group
        print(f"  [{self.record_id}] Record updated.")

    def display_info(self):
        status = "COMPLETE" if self.is_complete() else "IN PROGRESS"
        nxt = self.next_due_date()
        print(f"Record  : {self.record_id}")
        print(f"Age grp : {self.age_group}   District: {self.district}")
        print(f"Vaccine : {self.vaccine.name} "
              f"({len(self.doses_given)}/{self.vaccine.doses_required} doses)")
        print(f"Status  : {status}")
        if nxt:
            print(f"Next due: {nxt.isoformat()}")

    # ---- Class method -----------------------------------------------------
    @classmethod
    def get_total_records(cls):
        """Return how many records have been created."""
        return cls.total_records

    # ---- Static method ----------------------------------------------------
    @staticmethod
    def is_valid_id(record_id):
        """True if the ID has the form 'VR-' followed by exactly 3 digits."""
        return (isinstance(record_id, str) and len(record_id) == 6
                and record_id.startswith("VR-") and record_id[3:].isdigit())


# ---------------------------------------------------------------------------
# Task 2: DICTIONARY data structure + add / display functions
# Key = record ID, Value = VaccinationRecord object
# ---------------------------------------------------------------------------
def add_record(registry, record):
    """Add a record to the registry (dictionary). IDs must be unique."""
    if record.record_id in registry:
        print(f"  Cannot add: ID {record.record_id} already exists.")
        return False
    registry[record.record_id] = record
    VaccinationRecord.total_records += 1   # count only records actually stored
    print(f"  Added record {record.record_id}.")
    return True


def display_records(registry):
    """Loop through the registry and display every record."""
    if not registry:
        print("  No records yet.")
        return
    for record in registry.values():
        record.display_info()
        print("-" * 40)


# ---------------------------------------------------------------------------
# Demo (non-interactive) - shows all required features
# ---------------------------------------------------------------------------
def run_demo():
    registry = {}

    print("=== 1. Create Vaccine objects ===")
    polio = Vaccine("Polio (OPV)", 3, 28)
    measles = Vaccine("Measles", 2, 180)
    polio.display_info()
    print()
    measles.display_info()
    print(f"Vaccines created: {Vaccine.get_total_vaccines()}")

    print("\n=== 2. Create records and add to the dictionary ===")
    add_record(registry, VaccinationRecord("VR-001", "0-5", "Western Area Urban", polio))
    add_record(registry, VaccinationRecord("VR-002", "6-17", "Bo", measles))
    add_record(registry, VaccinationRecord("VR-003", "18-49", "Kenema", polio))
    add_record(registry, VaccinationRecord("VR-001", "0-5", "Bo", polio))  # duplicate

    print("\n=== 3. Static method: ID validation ===")
    for test_id in ("VR-004", "ABC-1", "VR-12"):
        print(f"  {test_id!r} valid? {VaccinationRecord.is_valid_id(test_id)}")

    print("\n=== 4. Record doses (object interaction) ===")
    registry["VR-001"].give_dose(date(2026, 10, 1))
    registry["VR-001"].give_dose(date(2026, 10, 29))
    registry["VR-002"].give_dose(date(2026, 10, 5))
    registry["VR-002"].give_dose(date(2027, 4, 3))
    registry["VR-002"].give_dose()          # already complete

    print("\n=== 5. Update a record ===")
    registry["VR-003"].update_record(district="Kono", age_group="50+")

    print("\n=== 6. Display all records ===")
    display_records(registry)

    print(f"\nTotal records (class method): {VaccinationRecord.get_total_records()}")


# ---------------------------------------------------------------------------
# Simple interactive menu (inclusive: plain text, numbered choices)
# ---------------------------------------------------------------------------
def run_menu():
    vaccines = {
        "1": Vaccine("Polio (OPV)", 3, 28),
        "2": Vaccine("Measles", 2, 180),
        "3": Vaccine("COVID-19", 2, 28),
    }
    registry = {}
    while True:
        print("\n--- Vaccination Tracker ---")
        print("1. Add record\n2. Record a dose\n3. Show all records\n4. Quit")
        choice = input("Choose 1-4: ").strip()
        if choice == "1":
            rid = input("Record ID (e.g. VR-001): ").strip()
            age = input(f"Age group {VaccinationRecord.AGE_GROUPS}: ").strip()
            district = input("District: ").strip()
            print("Vaccines: " + ", ".join(f"{k}={v.name}" for k, v in vaccines.items()))
            vac = vaccines.get(input("Vaccine number: ").strip())
            if vac is None:
                print("  Unknown vaccine.")
                continue
            try:
                add_record(registry, VaccinationRecord(rid, age, district, vac))
            except ValueError as err:
                print(f"  Error: {err}")
        elif choice == "2":
            rec = registry.get(input("Record ID: ").strip())
            if rec:
                rec.give_dose()
            else:
                print("  Record not found.")
        elif choice == "3":
            display_records(registry)
        elif choice == "4":
            print("Goodbye.")
            break
        else:
            print("  Please enter a number from 1 to 4.")


if __name__ == "__main__":
    import sys
    if "--menu" in sys.argv:
        run_menu()
    else:
        run_demo()
