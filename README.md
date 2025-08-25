# Patients

The `patients.py` is an utility that distibutes a number of patients on a set of doctors
randomly. The patients are distributed twice. The first time, the patients are distributed
evenly (as good as possible) using the `random.shuffle` function. The patients are then
distributed a second time where each patient is placed on a new doctor.

There are two  input files needed by  the utiliy. The first is a CSV file containing all
patients where the third column is expected to be the identifier and must be unique. The
second input is a text file with the names of all doctors. The names of the doctors needs
to be unique. 

The output from the utiliy is a CSV file that is identical to the input (patients) file
with two added columns, one for each doctor that the patient was assigned to.
