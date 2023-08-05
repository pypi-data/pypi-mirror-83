import sys
import time

from detectr.mvcmodel import MVCModelWatch


class MVCViewBase:
    def __init__(self, lines):
        self.lines = lines
        self.initialized = False
        self.created = int(time.time() * 1000)

    def update(self):
        if not self.initialized:
            print("\n" * (self.lines - 1))
        self.initialized = True
        sys.stdout.write("\033[" + str(self.lines) + "A")


class MVCViewLearn(MVCViewBase):
    def __init__(self, mvc_model):
        super().__init__(8)
        self.mvc_model = mvc_model

    def update(self):
        super().update()

        data = [
            self.mvc_model.uniq_system_calls(),
            self.mvc_model.uniq_sequences(),
            self.mvc_model.valid_entries(),
            self.mvc_model.invalid_entries(),
            self.mvc_model.pids()
        ]

        data = [str(i) for i in data]
        maxlen = max([5] + [len(entry) for entry in data])
        data = [" " * (maxlen - len(i)) + i for i in data]
        print("┌───────────────────────┬─{}─┐".format("─" * maxlen))
        print("│ Unique system calls   │ {} │".format(data[0]))
        print("│ Unique sequences      │ {} │".format(data[1]))
        print("│ System calls detected │ {} │".format(data[2]))
        print("│ Ignored lines         │ {} │".format(data[3]))
        print("│ Number of processes   │ {} │".format(data[4]))
        print("└───────────────────────┴─{}─┘".format("─" * maxlen))

        c = int(time.time() * 1000) - self.created
        if not self.mvc_model.stopped():
            if c % 1500 <= 1000:
                print("\033[1;44m\033[1;37m[\033[1;31m⬤ \033[1;37mREC]\033[0m")
            else:
                print("\033[1;44m\033[1;37m[\033[1;31m  \033[1;37mREC]\033[0m")
        else:
            print("\033[1;35m[\033[1;32m■\033[1;35m] \033[1;32mPROCESS EXITED\033[0m")


class MVCViewWatch(MVCViewBase):
    def __init__(self, mvc_model: MVCModelWatch):
        super().__init__(12)
        self.mvc_model = mvc_model

    def update(self):
        super().update()

        data = [
            self.mvc_model.uniq_system_calls(),
            self.mvc_model.uniq_sequences(),
            self.mvc_model.valid_entries(),
            self.mvc_model.invalid_entries(),
            self.mvc_model.pids(),
            self.mvc_model.matches(),
            self.mvc_model.mismatches(),
            self.mvc_model.alerts()
        ]
        data = [str(i) for i in data]
        maxlen = max([5] + [len(entry) for entry in data])
        data = [" " * (maxlen - len(i)) + i for i in data]
        print("┌───────────────────────┬─{}─┐".format("─" * maxlen))
        print("│ Unique system calls   │ {} │".format(data[0]))
        print("│ Unique sequences      │ {} │".format(data[1]))
        print("│ System calls detected │ {} │".format(data[2]))
        print("│ Ignored lines         │ {} │".format(data[3]))
        print("│ Number of processes   │ {} │".format(data[4]))
        print("├───────────────────────┼─{}─┤".format("─" * maxlen))
        print("│ Total matches         │ {} │".format(data[5]))
        print("│ Total mismatches      │ {} │".format(data[6]))
        if self.mvc_model.alerts() == 0:
            print("│ Alerts                │ {} │".format(data[7]))
        else:
            print("│ Alerts                │ \033[1;37;1;41m{}\033[0m │".format(data[7]))
        print("└───────────────────────┴─{}─┘".format("─" * maxlen))

        c = int(time.time() * 1000) - self.created
        if not self.mvc_model.stopped():
            if c % 1500 <= 1000:
                print("\033[1;44m\033[1;37m[\033[1;31m👀 \033[1;37mWATCHING]\033[0m")
            else:
                print("\033[1;44m\033[1;37m[\033[1;31m   \033[1;37mWATCHING]\033[0m")
        else:
            print("\033[1;35m[\033[1;32m■\033[1;35m] \033[1;32mPROCESS EXITED\033[0m")

