#!/usr/bin/env python3
import argparse
import csv
import random
import time

ID_POS = 2


class Patient:
    def __init__(self, row) -> None:
        self.id = row[ID_POS]
        self.data = row


class Doctor:
    def __init__(self, name) -> None:
        self.name = name
        self.patients_first = []
        self.patients_second = []


def read_doctor_data(input_file):
    """Open the doctor file (text) and create a dictionary of all the doctors"""
    doctors = dict()
    idx = 0
    with open(input_file, newline="") as f:
        for name in f:
            name = name.rstrip(" \t\n\r")
            if name:
                print(name)
                doctors[idx] = Doctor(name)
                idx += 1
    return doctors


def read_patient_data(input_file):
    """Open the csv file and return a dict of all patients (Patient objects) and the header"""
    patients = {}
    header = None
    with open(input_file, newline="") as csvfile:
        patient_reader = csv.reader(csvfile, delimiter=",", quotechar="|")
        for idx, row in enumerate(patient_reader):
            if idx == 0:
                header = row
            else:
                patient = Patient(row)
                patients[patient.id] = patient
    return header, patients


def write_patient_data(header, patients, output_file):
    """Write all patient data into the output_file, overwriting existing data.
    Add two output columns"""
    with open(output_file, "w", newline="") as csvfile:
        patient_writer = csv.writer(csvfile, delimiter=",", quotechar="|")
        header.extend(["DOCTOR 1", "DOCTOR 2"])
        patient_writer.writerow(header)
        for patient in patients.values():
            patient_writer.writerow(patient.data)


def distribute_first(patients, doctors):
    """Distribute evenly the list of patients on the doctors. Update the doctor's
    patients_first attribute accordingly."""
    patient_ids = [patient.id for patient in patients.values()]
    random.shuffle(patient_ids)
    base, extra = divmod(len(patient_ids), len(doctors))

    start = 0
    for i in range(len(doctors)):
        nof_patients = base + (1 if i < extra else 0)
        doctors[i].patients_first = patient_ids[start : start + nof_patients]
        start += nof_patients

    for doctor in doctors.values():
        for patient_id in doctor.patients_first:
            # Find patient and add doctor in first output column
            patients[patient_id].data.append(doctor.name)

    # TODO: Remove printout
    total_distributed = 0
    for _, d in doctors.items():
        print(f"Patients: {len(d.patients_first)}")
        total_distributed += len(d.patients_first)
    print(f"Distributed: {total_distributed}")


def distribute_second(patients, doctors):
    """Distribute the patients a second time. The patients shall be distributed
    evenly and randomly. No patient may end up at the same doctor as in the first
    round."""
    pass


def check_input(patients, doctors):
    """Return True if the input data is ok, i.e., no duplicates found etc. Any errors
    found are printed"""
    input_ok = True
    s = set()
    duplicates = set()
    for patient in patients.values():
        if patient.id not in s:
            s.add(patient.id)
        else:
            duplicates.add(patient.id)

    # Print all duplicate patients
    for duplicate_pat_id in duplicates:
        idx = []
        for i, patient in enumerate(patients):
            if patient.id == duplicate_pat_id:
                idx.append(i + 1)  # Add to convert from 0 indexing to 1 indexing
        print(
            f"Patient {duplicate_pat_id} found more than once (rows: {', '.join([str(i) for i in idx])})"
        )

    doctor_names = [doctor.name for doctor in doctors.values()]
    if len(set(doctor_names)) != len(doctors):
        input_ok = False
        print(f"Duplicate doctors found - check input file")

    if len(duplicates) != 0:
        input_ok = False

    print(f"Number of doctors: {len(doctors)}")
    print(f"Number of patients: {len(patients)} (unique: {len(s)})")
    return input_ok


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="patients",
        description="""
Utility that distibutes a number or patients on a set of doctors randomly. The patients
are distributed twice. The first time, the patients are distributed evenly (as good as
possible) using the `random.shuffle` function. The patients are then distributed a second
time. Each patient is then placed on a new doctor.""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "patients",
        help="""CSV file containing all patients. Column 2 is expected to be the identifier and must be unique""",
    )
    parser.add_argument(
        "doctors",
        help="""Text file containing the name of all doctors, one doctor's name per line""",
    )
    parser.add_argument(
        "output",
        help="""CSV file identical to the input (patients) file with two added columns, one for each doctor""",
    )
    parser.add_argument("--seed", "-s", type=int, help="Seed for the random generator")
    args = parser.parse_args()

    start_time = time.time()
    if args.seed:
        print(f"Seed provided ({args.seed})")
        random.seed(args.seed)

    doctors = read_doctor_data(args.doctors)
    header, patients = read_patient_data(args.patients)

    # Stop execution if any errors are found
    if not check_input(patients, doctors):
        exit()

    distribute_first(patients, doctors)
    distribute_second(patients, doctors)

    write_patient_data(header, patients, args.output)
    print("Finished in {} seconds".format(time.process_time()))
