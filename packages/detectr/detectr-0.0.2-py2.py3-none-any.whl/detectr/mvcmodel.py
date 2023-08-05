import unittest
import json

from detectr.mlmodel import MLModel
from detectr.piddetails import PidDetails
from detectr.parser import Parser, SystemCall
from detectr.tracealert import TraceAlert

SUFFIX_TRACE_LEN = 100
DEFAULT_SEQUENCE_LENGTH = 3
ALERT_MIN_TRACE_LEN = 50
ALERT_THRESHOLD = 0.1
ALERT_LOW_THRESHOLD = 0.08


class MVCModelBase:
    def __init__(self, sequence_length):
        self.sequence_length = sequence_length
        self.uniq_syscalls = set()
        self.n_lines_ok = 0   # number of lines with a valid system call
        self.n_lines_err = 0  # number of lines without a system call
        self._uniq_sequences = set()
        self.last_syscalls = {}
        self._stopped = False
        self._last_syscall = None
        self._pids = set()
        self._parser = Parser()

    # TODO test
    def reset_for_additional_trace(self):
        self.last_syscalls = {}
        self._last_syscall = None

    def _update_uniq_sequences(self, syscalls):
        if len(syscalls) >= self.sequence_length:
            sequence = syscalls[-self.sequence_length:]
            self._uniq_sequences.add(",".join(sequence))

    def _update_last_syscalls(self, syscall: SystemCall):
        pid = syscall.pid
        syscalls = self.last_syscalls.get(pid, [])
        syscalls.append(syscall.func)
        self._update_uniq_sequences(syscalls)
        self.last_syscalls[pid] = syscalls

    def add_line(self, line):
        syscall = self._parser.parse_line(line)
        if syscall is not None:
            self.n_lines_ok += 1
            self.uniq_syscalls.add(syscall.func)
            self._update_last_syscalls(syscall)
            self._pids.add(syscall.pid)
        else:
            self.n_lines_err += 1
        self._last_syscall = syscall # TODO: write a test

    def uniq_system_calls(self):
        return len(self.uniq_syscalls)

    def valid_entries(self):
        return self.n_lines_ok

    def invalid_entries(self):
        return self.n_lines_err

    def uniq_sequences(self):
        return len(self._uniq_sequences)

    def stop(self):
        self._stopped = True

    def stopped(self):
        return self._stopped

    def pids(self):
        return len(self._pids)


class MVCModelLearn(MVCModelBase):
    def __init__(self, sequence_length=DEFAULT_SEQUENCE_LENGTH):
        super().__init__(sequence_length)

    def model(self):
        data = {
            "sequences": list(self._uniq_sequences),
            "sequence_length": self.sequence_length
        }
        return json.dumps(data)


class MVCModelWatch(MVCModelBase):
    def __init__(
            self,
            model: MLModel,
            suffix_trace_len=SUFFIX_TRACE_LEN,
            alert_threshold=ALERT_THRESHOLD,
            alert_low_threshold=ALERT_LOW_THRESHOLD,
            alert_min_trace_len=ALERT_MIN_TRACE_LEN
    ):
        super().__init__(model.sequence_length())
        self._mlmodel = model
        self._n_mismatches = 0
        self._n_matches = 0
        self._pid_details = {}
        self._suffix_trace_len = suffix_trace_len
        self._alerts = 0
        self._alert_threshold = alert_threshold
        self._alert_low_threshold = alert_low_threshold
        self._alert_min_trace_len = alert_min_trace_len
        self._tracer = TraceAlert()

    def add_line(self, line):
        super().add_line(line)
        if self._last_syscall is not None:
            self._classification(self._last_syscall)

    def _has_required_trace_len(self, pid_details: PidDetails):
        return pid_details.len_trace() >= self._alert_min_trace_len

    # sobald der threshold überschritten wird => alarm
    # nach einem alarm muss das verhältnis auf mindestens unter ALERT_LOW_THRESHOLD
    # runter gehen bevor ein neuer alarm gemeldet wird
    def _check_alert(self, pid_details: PidDetails):
        if not self._has_required_trace_len(pid_details):
            return
        r = pid_details.score()
        if r <= self._alert_low_threshold:
            pid_details.alert_enabled = True
            self._tracer.disable_tracing(pid_details.pid)
        if not pid_details.alert_enabled or r < self._alert_threshold:
            return
        # Do not report a new alert until r is below ALERT_LOW_THRESHOLD
        pid_details.alert_enabled = False
        self._alerts += 1
        self._tracer.enable_tracing(pid_details.pid)

    def _classification(self, syscall: SystemCall):
        pid = syscall.pid
        pid_details = self._pid_details.get(
            pid, PidDetails(suffix_trace_len=self._suffix_trace_len, pid=pid)
        )
        pid_details.inc_trace_len()
        trace = self.last_syscalls.get(pid, [])
        if len(trace) >= self.sequence_length:
            sequence = trace[-self.sequence_length:]
            anomaly = False
            if self._mlmodel.is_anomaly(sequence):
                self._n_mismatches += 1
                pid_details.inc_mismatch()
                anomaly = True
            else:
                self._n_matches += 1
                pid_details.inc_match()
            # We also have to call _check_alert for sequences that are not anomalies
            # so that ...
            self._check_alert(pid_details)
            # Call on _tracer needs to be done after _check_alert.
            self._tracer.add_syscall(
                pid_details=pid_details, syscall=syscall, anomaly=anomaly
            )
        self._pid_details[pid] = pid_details

    def mismatches(self):
        return self._n_mismatches

    def matches(self):
        return self._n_matches

    def pid_details(self, pid):
        return self._pid_details.get(pid, None)

    def alerts(self):
        return self._alerts


# -------------------------------------------------------


class MVCModelWatchTest(unittest.TestCase):
    def test_add_line(self):
        m = MLModel(3)
        s = MVCModelWatch(m)
        s.add_line('openat(AT_FDCWD, ...')
        self.assertEqual(s.mismatches(), 0)
        s.add_line('foo(AT_FDCWD, ...')
        self.assertEqual(s.mismatches(), 0)
        s.add_line('bar(AT_FDCWD, ...')
        self.assertEqual(s.mismatches(), 1)
        self.assertEqual(s.matches(), 0)

    def test_matches(self):
        m = MLModel.from_sequences([["a","b","c"], ["d","e","f"]])
        s = MVCModelWatch(m)
        s.add_line('openat(AT_FDCWD, ...')
        self.assertEqual(s.mismatches(), 0)
        s.add_line('foo(AT_FDCWD, ...')
        self.assertEqual(s.mismatches(), 0)
        s.add_line('bar(AT_FDCWD, ...')
        self.assertEqual(s.mismatches(), 1)
        s.add_line('a(AT_FDCWD, ...')
        self.assertEqual(s.mismatches(), 2)
        s.add_line('b(AT_FDCWD, ...')
        self.assertEqual(s.mismatches(), 3)
        self.assertEqual(s.matches(), 0)
        s.add_line('c(AT_FDCWD, ...')
        self.assertEqual(s.mismatches(), 3)
        self.assertEqual(s.matches(), 1)
        s.add_line('d(AT_FDCWD, ...')
        self.assertEqual(s.mismatches(), 4)
        self.assertEqual(s.matches(), 1)

    def test_classification(self):
        m = MLModel.from_sequences([["a","b","c"], ["d","e","f"]])
        s = MVCModelWatch(m, suffix_trace_len=3)
        s.add_line('d(AT_FDCWD, ...')
        s.add_line('e(AT_FDCWD, ...')
        self.assertEqual(s.pid_details(0).len_trace(), 2)
        self.assertEqual(s.pid_details(0).total_mismatches(), 0)
        self.assertEqual(s.pid_details(0).suffix_trace, [])
        s.add_line('d(AT_FDCWD, ...')
        self.assertEqual(s.pid_details(0).len_trace(), 3)
        self.assertEqual(s.pid_details(0).total_mismatches(), 1)
        self.assertEqual(s.pid_details(0).suffix_trace, [True])
        s.add_line('e(AT_FDCWD, ...')
        self.assertEqual(s.pid_details(0).len_trace(), 4)
        self.assertEqual(s.pid_details(0).total_mismatches(), 2)
        self.assertEqual(s.pid_details(0).suffix_trace, [True, True])
        s.add_line('f(AT_FDCWD, ...')
        self.assertEqual(s.pid_details(0).len_trace(), 5)
        self.assertEqual(s.pid_details(0).total_mismatches(), 2)
        self.assertEqual(s.pid_details(0).suffix_mismatches(), 2)
        self.assertEqual(s.pid_details(0).suffix_trace, [True, True, False])
        s.add_line('f(AT_FDCWD, ...')
        self.assertEqual(s.pid_details(0).len_trace(), 6)
        self.assertEqual(s.pid_details(0).total_mismatches(), 3)
        self.assertEqual(s.pid_details(0).suffix_mismatches(), 2)
        self.assertEqual(s.pid_details(0).suffix_trace, [True, True, False])

    def test_check_alert(self):
        m = MLModel.from_sequences([["a","b"], ["d","e"], ["e", "e"]])
        s = MVCModelWatch(
            m, suffix_trace_len=10, alert_threshold=0.5, alert_low_threshold=0.2,
            alert_min_trace_len=10
        )
        s.add_line('d(AT_FDCWD, ...')
        self.assertFalse(s._has_required_trace_len(s.pid_details(0)))
        self.assertTrue(s.pid_details(0).alert_enabled)
        s.add_line('d(AT_FDCWD, ...')  # F
        s.add_line('d(AT_FDCWD, ...')  # FF
        s.add_line('d(AT_FDCWD, ...')  # FFF
        self.assertEqual(s.pid_details(0).suffix_len(), 3)
        self.assertEqual(s.alerts(), 0)
        s.add_line('d(AT_FDCWD, ...')  # FFFF
        self.assertEqual(s.alerts(), 0)
        s.add_line('d(AT_FDCWD, ...')  # FFFFF
        self.assertEqual(s.alerts(), 0)
        s.add_line('d(AT_FDCWD, ...')  # FFFFF F
        self.assertEqual(s.alerts(), 0)
        s.add_line('d(AT_FDCWD, ...')  # FFFFF FF
        self.assertEqual(s.alerts(), 0)
        s.add_line('d(AT_FDCWD, ...')  # FFFFF FFF
        self.assertFalse(s._has_required_trace_len(s.pid_details(0)))
        self.assertEqual(s.alerts(), 0)
        self.assertTrue(s.pid_details(0).alert_enabled)
        s.add_line('d(AT_FDCWD, ...')  # FFFFF FFFF
        self.assertTrue(s._has_required_trace_len(s.pid_details(0)))
        self.assertAlmostEqual(s.pid_details(0).score(), 1.0)
        self.assertEqual(s.pid_details(0).suffix_len(), 9)
        self.assertEqual(s.pid_details(0).len_trace(), 10)
        self.assertFalse(s.pid_details(0).alert_enabled)
        self.assertEqual(s.alerts(), 1)
        s.add_line('d(AT_FDCWD, ...')  # FFFFF FFFFF
        self.assertAlmostEqual(s.pid_details(0).score(), 1.0)
        self.assertEqual(s.pid_details(0).suffix_len(), 10)
        self.assertEqual(s.pid_details(0).len_trace(), 11)
        self.assertFalse(s.pid_details(0).alert_enabled)
        self.assertEqual(s.alerts(), 1)
        s.add_line('e(AT_FDCWD, ...')  # FFFFF FFFFT
        self.assertAlmostEqual(s.pid_details(0).score(), 0.9)
        self.assertEqual(s.pid_details(0).suffix_len(), 10)
        self.assertEqual(s.pid_details(0).len_trace(), 12)
        self.assertFalse(s.pid_details(0).alert_enabled)
        self.assertEqual(s.alerts(), 1)
        s.add_line('e(AT_FDCWD, ...')  # FFFFF FFFTT
        self.assertAlmostEqual(s.pid_details(0).score(), 0.8)
        self.assertEqual(s.pid_details(0).suffix_len(), 10)
        self.assertEqual(s.pid_details(0).len_trace(), 13)
        self.assertFalse(s.pid_details(0).alert_enabled)
        self.assertEqual(s.alerts(), 1)
        for _ in range(5):
            s.add_line('e(AT_FDCWD, ...')  # FFFTT TTTTT
        self.assertAlmostEqual(s.pid_details(0).score(), 0.3)
        self.assertFalse(s.pid_details(0).alert_enabled)
        self.assertEqual(s.alerts(), 1)
        s.add_line('e(AT_FDCWD, ...')  # FFTTT TTTTT
        self.assertAlmostEqual(s.pid_details(0).score(), 0.2)
        self.assertTrue(s.pid_details(0).alert_enabled)
        self.assertEqual(s.alerts(), 1)
        s.add_line('z(AT_FDCWD, ...')  # FTTTT TTTTF
        self.assertAlmostEqual(s.pid_details(0).score(), 0.2)
        self.assertTrue(s.pid_details(0).alert_enabled)
        self.assertEqual(s.alerts(), 1)
        s.add_line('z(AT_FDCWD, ...')  # TTTTT TTTFF
        self.assertAlmostEqual(s.pid_details(0).score(), 0.2)
        self.assertTrue(s.pid_details(0).alert_enabled)
        self.assertEqual(s.alerts(), 1)
        s.add_line('z(AT_FDCWD, ...')  # TTTTT TTFFF
        self.assertAlmostEqual(s.pid_details(0).score(), 0.3)
        self.assertTrue(s.pid_details(0).alert_enabled)
        self.assertEqual(s.alerts(), 1)
        s.add_line('e(AT_FDCWD, ...')  # TTTTT TFFFF
        self.assertAlmostEqual(s.pid_details(0).score(), 0.4)
        self.assertTrue(s.pid_details(0).alert_enabled)
        self.assertEqual(s.alerts(), 1)
        s.add_line('e(AT_FDCWD, ...')  # TTTTT FFFFT
        self.assertAlmostEqual(s.pid_details(0).score(), 0.4)
        self.assertTrue(s.pid_details(0).alert_enabled)
        self.assertEqual(s.alerts(), 1)
        s.add_line('z(AT_FDCWD, ...')  # TTTTF FFFTF
        self.assertAlmostEqual(s.pid_details(0).score(), 0.5)
        self.assertFalse(s.pid_details(0).alert_enabled)
        self.assertEqual(s.alerts(), 2)
        s.add_line('z(AT_FDCWD, ...')  # TTTFF FFTFF
        self.assertAlmostEqual(s.pid_details(0).score(), 0.6)
        self.assertFalse(s.pid_details(0).alert_enabled)
        self.assertEqual(s.alerts(), 2)


class MVCModelBaseTest(unittest.TestCase):
    def test_add_line(self):
        s = MVCModelLearn()
        line = 'openat(AT_FDCWD, "/etc/passwd", O_RDONLY | O_CLOEXEC) = 11\n'
        s.add_line(line)
        self.assertEqual(s.n_lines_ok, 1)
        self.assertSetEqual(s.uniq_syscalls, {"openat"})
        self.assertEqual(s._last_syscall.pid, 0)
        self.assertEqual(s._last_syscall.func, "openat")

        line = 'lseek(11, 0, SEEK_CUR)                  = 0'
        s.add_line(line)
        self.assertSetEqual(s.uniq_syscalls, {"openat", "lseek"})
        self.assertEqual(s.n_lines_ok, 2)
        self.assertEqual(s.n_lines_err, 0)
        self.assertEqual(s._last_syscall.pid, 0)
        self.assertEqual(s._last_syscall.func, "lseek")

        line = '21866 <... getpid resumed> )'
        s.add_line(line)
        self.assertEqual(s.n_lines_ok, 2)
        self.assertEqual(s.n_lines_err, 1)
        self.assertIsNone(s._last_syscall)

    def test_update_last_syscalls(self):
        # test update_last_syscall via add_line
        s = MVCModelLearn()
        s.add_line('openat(AT_FDCWD, "/etc/passwd", O_RDONLY | O_CLOEXEC) = 11\n')
        self.assertListEqual(s.last_syscalls[0], ["openat"])
        s.add_line('foo(AT_FDCWD, "/etc/passwd", O_RDONLY | O_CLOEXEC) = 11\n')
        self.assertListEqual(s.last_syscalls[0], ["openat", "foo"])

        s.add_line('123 bar(AT_FDCWD, "/etc/passwd", O_RDONLY | O_CLOEXEC) = 11\n')
        self.assertListEqual(s.last_syscalls[0], ["openat", "foo"])
        self.assertListEqual(s.last_syscalls[123], ["bar"])

    def test_update_uniq_sequences(self):
        # test update_uniq_sequences via add_line
        s = MVCModelLearn()
        s.add_line('openat(AT_FDCWD, "/etc/passwd", O_RDONLY | O_CLOEXEC) = 11\n')
        s.add_line('foo(AT_FDCWD, "/etc/passwd", O_RDONLY | O_CLOEXEC) = 11\n')
        self.assertSetEqual(s._uniq_sequences, set())
        s.add_line('bar(AT_FDCWD, "/etc/passwd", O_RDONLY | O_CLOEXEC) = 11\n')
        self.assertSetEqual(s._uniq_sequences, {"openat,foo,bar"})
        s.add_line('baz(AT_FDCWD, "/etc/passwd", O_RDONLY | O_CLOEXEC) = 11\n')
        self.assertSetEqual(s._uniq_sequences, {"openat,foo,bar", "foo,bar,baz"})

        s.add_line('123 aaa(AT_FDCWD, "/etc/passwd", O_RDONLY | O_CLOEXEC) = 11\n')
        s.add_line('123 bbb(AT_FDCWD, "/etc/passwd", O_RDONLY | O_CLOEXEC) = 11\n')
        self.assertSetEqual(s._uniq_sequences, {"openat,foo,bar", "foo,bar,baz"})
        s.add_line('123 ccc(AT_FDCWD, "/etc/passwd", O_RDONLY | O_CLOEXEC) = 11\n')
        self.assertSetEqual(s._uniq_sequences, {"openat,foo,bar", "foo,bar,baz", "aaa,bbb,ccc"})

        s.add_line('baz(AT_FDCWD, "/etc/passwd", O_RDONLY | O_CLOEXEC) = 11\n')
        self.assertSetEqual(
            s._uniq_sequences,
            {"openat,foo,bar", "foo,bar,baz", "aaa,bbb,ccc", "bar,baz,baz"}
        )

        s.add_line('123 ddd(AT_FDCWD, "/etc/passwd", O_RDONLY | O_CLOEXEC) = 11\n')
        self.assertSetEqual(
            s._uniq_sequences,
            {"openat,foo,bar", "foo,bar,baz", "aaa,bbb,ccc", "bar,baz,baz", "bbb,ccc,ddd"}
        )

    def test_pids(self):
        s = MVCModelBase(3)
        s.add_line('123 ddd(AT_FDCWD, ...')
        self.assertEqual(s.pids(), 1)
        s.add_line('123 aaa(AT_FDCWD, ...')
        self.assertEqual(s.pids(), 1)
        s.add_line('1234 aaa(AT_FDCWD, ...')
        self.assertEqual(s.pids(), 2)


if __name__ == '__main__':
    unittest.main()

