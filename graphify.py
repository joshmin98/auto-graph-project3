import re
import sys
import random
import numpy as np
import matplotlib.pyplot as plt

target_file = sys.argv[1]
output_file = sys.argv[2]

procs_raw = []
procs = []
proc_num = 0;

class Proc:
    def __init__(self, text):
        global proc_num
        self.start_tick = []
        self.duration = []
        self.priority = []
        self.name = ""
        self.color = ""

        # Get proc name from header data
        name_regex = re.compile('name\ =\ (.*),\ pid\ =\ (\d+)')
        pid = 0
        for result in re.findall('[\*]+(.*?)[\*]+', text, re.S):
            (self.name, pid) = name_regex.findall(result)[0]
        random.seed(proc_num)
        rand_color = random.randint(0, 16777215)
        self.color = (f'#{hex(rand_color)[2:]}')
        proc_num = proc_num + 1;

        # Get stat info
        stat_regex = re.compile('\d+')
        for line in text.split('\n')[7:]:
            stats = stat_regex.findall(line)
            if len(stats) is 3:
                self.start_tick.append(int(stats[0]))
                self.duration.append(int(stats[1]))
                self.priority.append(int(stats[2]))


# Get all pstat output
with open(target_file, "r") as raw:
    for result in re.findall('PSTAT_START(.*?)PSTAT_END', raw.read(), re.S):
        procs_raw.append(result)

# Parse output into internal data structure
for proc_text in procs_raw:
    procs.append(Proc(proc_text))

# Graph
fig, ax = plt.subplots()
ax.grid(True)

for proc in procs:
    for i in range(len(proc.priority)):
        ax.broken_barh([(proc.start_tick[i], proc.duration[i])],
                       (proc.priority[i], 1),
                       facecolors=proc.color
        )

ax.set_ylim(0, 3)
ax.set_yticklabels(("Q0", "Q1", "Q2"))
ax.set_yticks(np.arange(3))
ax.invert_yaxis()
plt.savefig(output_file)
