import unittest


class PidDetails:
    def __init__(
            self,
            suffix_trace_len,
            pid,
            len_trace=0,
            mismatched=0,
            ):
        self._len_trace = len_trace
        self.total_mismatched = mismatched
        self.suffix_trace = []  # ring buffer
        self.suffix_pos = 0
        self.suffix_mismatched = 0  # number of mismatches (i.e. #True) in suffix_trace
        self.suffix_trace_len = suffix_trace_len
        self.alert_enabled = True
        self.pid = pid

    def inc_trace_len(self):
        self._len_trace += 1

    def _inc_suffix(self, is_mismatch):
        if len(self.suffix_trace) < self.suffix_trace_len:
            # If length of suffix is smaller then the allowed one append.
            self.suffix_trace.append(is_mismatch)
        else:
            # Otherwise reduce ring buffer.
            current_value = self.suffix_trace[self.suffix_pos]
            if current_value:
                self.suffix_mismatched -= 1
            self.suffix_trace[self.suffix_pos] = is_mismatch
            self.suffix_pos = (self.suffix_pos + 1) % self.suffix_trace_len
        if is_mismatch:
            self.suffix_mismatched += 1

    def inc_match(self):
        self._inc_suffix(False)

    def inc_mismatch(self):
        self.total_mismatched += 1
        self._inc_suffix(True)

    def total_mismatches(self):
        return self.total_mismatched

    def len_trace(self):
        return self._len_trace

    def suffix_mismatches(self):
        return self.suffix_mismatched

    def suffix_len(self):
        return len(self.suffix_trace)

    def score(self):
        if self.suffix_len() == 0:
            return 0
        return self.suffix_mismatches() / self.suffix_len()


class PidDetailsTest(unittest.TestCase):
    def test_score(self):
        s = PidDetails(suffix_trace_len=5, pid=123)
        s.inc_mismatch()
        s.inc_match()
        s.inc_match()
        self.assertAlmostEqual(1/3, s.score())
        s.inc_match()
        self.assertAlmostEqual(1/4, s.score())
        s.inc_match()
        self.assertAlmostEqual(1/5, s.score())
        s.inc_mismatch()
        self.assertAlmostEqual(1/5, s.score())
        s.inc_mismatch()
        self.assertAlmostEqual(2/5, s.score())

    def test_inc_trace(self):
        p = PidDetails(suffix_trace_len=100, pid=123)
        self.assertEqual(p.len_trace(), 0)
        p.inc_trace_len()
        self.assertEqual(p.len_trace(), 1)
        self.assertEqual(p.total_mismatches(), 0)

    def test_inc_mismatch(self):
        p = PidDetails(suffix_trace_len=3, pid=123)
        for i in range(3):
            p.inc_mismatch()
            self.assertEqual(p.total_mismatches(), i + 1)
            self.assertEqual(p.suffix_mismatches(), i + 1)
            self.assertEqual(p.suffix_len(), i + 1)
        # F,F,F

        p.inc_mismatch()
        # F,F,F,F
        self.assertEqual(p.total_mismatches(), 4)
        self.assertEqual(p.suffix_mismatches(), 3)
        self.assertEqual(p.suffix_len(), 3)

        p.inc_match()
        # F,F,F,F,T
        self.assertEqual(p.total_mismatches(), 4)
        self.assertEqual(p.suffix_mismatches(), 2)
        self.assertEqual(p.suffix_len(), 3)

        p.inc_match()
        # F,F,F,F,T,T
        self.assertEqual(p.total_mismatches(), 4)
        self.assertEqual(p.suffix_mismatches(), 1)
        self.assertEqual(p.suffix_len(), 3)

        p.inc_mismatch()
        # F,F,F,F,T,T,F
        self.assertEqual(p.total_mismatches(), 5)
        self.assertEqual(p.suffix_mismatches(), 1)
        self.assertEqual(p.suffix_len(), 3)

        p.inc_mismatch()
        # F,F,F,F,T,T,F,F
        self.assertEqual(p.total_mismatches(), 6)
        self.assertEqual(p.suffix_mismatches(), 2)
        self.assertEqual(p.suffix_len(), 3)

        p.inc_match()
        # F,F,F,F,T,T,F,F,T
        self.assertEqual(p.total_mismatches(), 6)
        self.assertEqual(p.suffix_mismatches(), 2)
        self.assertEqual(p.suffix_len(), 3)

        p.inc_mismatch()
        # F,F,F,F,T,T,F,F,T,F
        self.assertEqual(p.total_mismatches(), 7)
        self.assertEqual(p.suffix_mismatches(), 2)
        self.assertEqual(p.suffix_len(), 3)


if __name__ == "__main__":
    unittest.main()