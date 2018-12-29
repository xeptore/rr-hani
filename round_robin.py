import queue
import sys

"""
Parse string to non-negetive integer.
Returns converted number if successful, exits from the process otherwise
"""


def parse_abs_int(s):
    try:
        o = int(s)
        if o < 0:
            raise ValueError()
        return o
    except ValueError:
        print("\nInvalid Input.")
        print("Exiting...\n")
        sys.exit(1)


class Process:
    def __init__(self, arrTime, execTime):
        self.Arrival = arrTime
        self.OrigArrival = self.Arrival
        self.Execution = execTime
        self.Response = 0
        self.TotalResponse = 0
        self.Wait = 0
        self.TurnAround = 0


class ProcessPart:
    def __init__(self, begin, length):
        self.Begin = begin
        self.Length = length


# quantum
qtm = parse_abs_int(input("Enter Quantum Size: "))
# number of processes
pn = parse_abs_int(input("Enter Number Of Processes: "))
# processes parts queue
psq = [list() for i in range(pn)]
# list of proccesses
ps = list()
# fill processes information and append them to processes list
for i in range(pn):
    print("\nProcess", str(i + 1) + ":")
    arr = parse_abs_int(input("{:22}".format("  * Arrival Time: ")))
    exe = parse_abs_int(input("{:22}".format("  * Execution Time: ")))
    ps.append(Process(arr, exe))

# sorts processes by their arrival time
ps.sort(key=lambda p: p.Arrival)

# removes any existance time offset from processes start time
ofst = ps[0].Arrival
for p in ps:
    p.Arrival -= ofst
    p.OrigArrival -= ofst


# pushed processes forward to next nearest quantum time
for p in ps[1:]:
    t = 1 + p.Arrival // qtm
    p.Wait += t * qtm - p.Arrival
    p.Arrival = t * qtm

# set first response time of processes by the time they waited to now
for p in ps:
    p.Response = p.Wait

# split processes into parts by quantum length and append them to processes parts queue
total_parts = 0
for i, p in enumerate(ps):
    [psq[i].append(ProcessPart(p.Arrival + x * qtm, qtm))
     for x in range(p.Execution // qtm)]
    if p.Execution % qtm != 0:
        psq[i].append(
            ProcessPart(
                p.Arrival + (p.Execution // qtm) * qtm,
                p.Execution % qtm
            )
        )
    total_parts += len(psq[i])

# start from the end of the execution time and fill out the proccesses execution history list
cursor = sum([p.Execution for p in ps])
psx = [list() for i in psq]
while total_parts > 0:
    for i in reversed(range(pn)):
        if len(psq[i]) == 0:
            continue
        psx[i].append([cursor - psq[i][len(psq[i]) - 1].Length, cursor])
        cursor -= psq[i][len(psq[i]) - 1].Length
        total_parts -= 1
        psq[i].pop()

# order processes execution history incrementally
[ph.sort(key=lambda h: h[0]) for ph in psx]

# calculates processes total wait time and turn-around times
for i, p in enumerate(ps):
    p.TurnAround = psx[i][len(psx[i]) - 1][1] - p.OrigArrival
    p.TotalResponse = p.TurnAround - p.Response
    for k, v in enumerate(psx[i][1:], 1):
        p.Wait += v[0] - psx[i][k - 1][1]

print("\n\n")
print("{:35}".format(" -> First Response Time Average:"),
      "{:.2f}".format(sum([p.Response for p in ps]) / pn))
print("{:35}".format(" -> Total Response Time Average:"),
      "{:.2f}".format(sum([p.TotalResponse for p in ps]) / pn))
print("{:35}".format(" -> Wait Time Average:"),
      "{:.2f}".format(sum([p.Wait for p in ps]) / pn))
print("{:35}".format(" -> Turn Around Time Average:"),
      "{:.2f}".format(sum([p.TurnAround for p in ps]) / pn))
print("\n\n")
