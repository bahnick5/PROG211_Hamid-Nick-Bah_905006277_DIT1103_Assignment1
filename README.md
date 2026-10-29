# Vaccination Tracker

**Module:** PROG211 – Object-Oriented Programming 1
**Assignment:** Real-World Solutions under DPG Standards
**Domain:** Health – Vaccination Tracker
**Language:** Python 3 (standard library only)

A small, privacy-respecting program that tracks which vaccine doses people have received, whether their course is complete, and when the next dose is due.

## How to run

```bash
python3 vaccination_tracker.py          # runs the demo
python3 vaccination_tracker.py --menu   # interactive text menu
```

No installation or extra packages are needed.

## Project structure

| Item | Purpose |
|---|---|
| `vaccination_tracker.py` | All source code |
| `demo_output.txt` | Sample output of the demo |
| `README.md` | This file |

## How the code meets the tasks

**Task 1 – OOP basics.** Two classes: `Vaccine` (name, doses required, interval) and `VaccinationRecord` (record ID, age group, district, vaccine, doses given). Each has attributes and methods such as `display_info()` and `update_record()`. Objects interact: a `VaccinationRecord` holds a `Vaccine` object and uses its schedule to work out the next due date.

**Task 2 – Data structure.** A **dictionary** (`registry`) stores records with the unique record ID as the key. `add_record()` adds a record (rejecting duplicate IDs) and `display_records()` loops through the dictionary. A **tuple** (`dose_schedule`) is also used, as it never changes once created (optional extra marks).

**Task 3 – Methods.**
- Instance methods: `give_dose()`, `is_complete()`, `next_due_date()`, `update_record()`, `display_info()`
- Class methods (`@classmethod`): `Vaccine.get_total_vaccines()`, `VaccinationRecord.get_total_records()`
- Static method (`@staticmethod`): `VaccinationRecord.is_valid_id()`

## Alignment with Digital Public Goods (DPG) standards

| DPG principle | How this solution follows it |
|---|---|
| **Open-source** | Plain Python with no paid dependencies, uploaded to a public GitHub repository for anyone to use, study and improve. |
| **Inclusive and accessible design** | Simple numbered text menus, short plain-language messages and clear error messages. Works in any terminal with no special hardware, colour or fast internet. |
| **Privacy-respecting** | No names, phone numbers, addresses or national IDs are stored. Each person is only an anonymous ID (e.g. `VR-001`), an age *group* and a district. |
| **Modular and reusable** | `Vaccine` and `VaccinationRecord` are independent classes that can be imported into other health programs. Adding a new vaccine needs no code change in the classes. |

## Example usage

Sample input (menu mode):
```
Record ID (e.g. VR-001): VR-010
Age group ('0-5', '6-17', '18-49', '50+'): 0-5
District: Bo
Vaccine number: 1
```

Sample output:
```
  Added record VR-010.
```

Full demo output is in `demo_output.txt`, for example:
```
Record  : VR-001
Age grp : 0-5   District: Western Area Urban
Vaccine : Polio (OPV) (2/3 doses)
Status  : IN PROGRESS
Next due: 2026-11-26
```

## Author

Student, Limkokwing University of Creative Technology, Sierra Leone
Examiner: Amandus Benjamin Coker
