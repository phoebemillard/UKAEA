Use Tools along with 'Creates database for multiple pulses', 'Creates database for one pulse', and 'Compares database to EFIT'

These codes were written by Phoebe Millard between July 2023 and Janurary 2024

Overview of each file in this Final codes branch:

Tools: Python file containing all of the functions required to identify unstable modes from JET magnetic data, determine their toroidal mode number and q value, and output this to a database

Creates database for multiple pulses:The code uses the functions in 'Tools' to output a database containing the times, frequencies, toroidal mode numbers, experimental q values and q values predicted by equillibrium reconstruction codes such as EFIT of instabilities present in multiple JET pulses

Creates database for one pulse: The code uses the functions in 'Tools' to output a database containing the times, frequencies, toroidal mode numbers, experimental q values and q values predicted by equillibrium reconstruction codes such as EFIT of instabilities present in one JET pulse

Compares database to equillibrium reconstruction codes: Uses the database outputted using one or multiple JET pulses and calculates the relative error of the q profile predicted by EFIT, EFTM, EFTF and EFTP with respect to the experimenal q values calculated by the new programme. It can be used to show the relative error as a funtion of plasma radius or a histogram which can be used to compare the accuracy of the odfferent reconstruction codes. 

