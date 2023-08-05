import collections
import unittest
import time

from detectr.parser import SystemCall
from detectr.piddetails import PidDetails


class AlertEntry():
    def __init__(
            self,
            pid: int,
            funcname: str,
            line: str,
            anomaly: bool,
            score: float
            ):
        self._time = int(time.time() * 1000)  # time in ms
        self._pid = pid
        self._funcname = funcname
        self._line = line
        self._anomaly = anomaly
        self._score = score

    def as_dict(self):
        data = {
            "pid": self.pid,
            "function": self._funcname,
            "line": self._line,
            "anomaly": "yes" if self._anomaly else "no",
            "score": self.score
        }
        return data

# TODO: show the sequence which is an anomaly + the position in the sequence

# TODO: return all events
#       so that they can be written into a logfile or via rest api)


Trace = collections.namedtuple("Alert", "pid, trace")


class TraceAlert():
    def __init__(self):
        self._enabled_pids = {}
        self._finished = []

    def enable_tracing(self, pid):
        self._enabled_pids[pid] = []

    def disable_tracing(self, pid):
        if pid in self._enabled_pids:
            self._finished.append(Trace(pid=pid, trace=self._enabled_pids[pid]))
            del self._enabled_pids[pid]
            return True
        return False

    def add_syscall(self, pid_details: PidDetails, syscall: SystemCall, anomaly=False):
        if pid_details.pid not in self._enabled_pids:
            return False
        e = AlertEntry(
            pid=syscall.pid,
            funcname=syscall.func,
            line=syscall.line,
            anomaly=anomaly,
            score=pid_details.score()
        )
        self._enabled_pids[pid_details.pid].append(e)
        return True


# ----------- TESTS -----------------------------------------------------------------------


class TraceAlertTest(unittest.TestCase):
    def test_enable_disable(self):
        t = TraceAlert()
        self.assertFalse(t.disable_tracing(123))

        t.enable_tracing(456)
        self.assertTrue(t.disable_tracing(456))
        self.assertFalse(t.disable_tracing(456))

        t = TraceAlert()
        t.enable_tracing(1234)
        pid_details = PidDetails(suffix_trace_len=10, pid=1234)
        syscall = SystemCall(idx=0, pid=1234, func="openat1", line="openat(AT_FDCWD, ...")
        t.add_syscall(pid_details=pid_details, syscall=syscall)
        syscall = SystemCall(idx=0, pid=1234, func="openat2", line="openat(AT_FDCWD, ...")
        t.add_syscall(pid_details=pid_details, syscall=syscall)
        self.assertEqual(len(t._finished), 0)
        t.disable_tracing(1234)
        self.assertEqual(len(t._finished), 1)
        self.assertEqual(t._finished[0].pid, 1234)
        self.assertEqual(t._finished[0].trace[0]._funcname, "openat1")
        self.assertEqual(len(t._finished[0].trace), 2)
        self.assertEqual(t._finished[0].trace[1]._funcname, "openat2")

    def test_add_syscall(self):
        t = TraceAlert()

        t.enable_tracing(12)
        pid_details = PidDetails(suffix_trace_len=10, pid=12)
        syscall = SystemCall(idx=0, pid=12, func="openat", line="openat(AT_FDCWD, ...")
        self.assertTrue(t.add_syscall(pid_details=pid_details, syscall=syscall))
        self.assertEqual(len(t._enabled_pids[12]), 1)

        pid_details = PidDetails(suffix_trace_len=10, pid=123)
        self.assertFalse(t.add_syscall(pid_details=pid_details, syscall=syscall))

        pid_details = PidDetails(suffix_trace_len=10, pid=12)
        self.assertTrue(t.add_syscall(pid_details=pid_details, syscall=syscall))
        self.assertEqual(len(t._enabled_pids[12]), 2)

