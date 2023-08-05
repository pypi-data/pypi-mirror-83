import re
import collections
import unittest


SystemCall = collections.namedtuple('SystemCall', "idx, pid, func, line")


class Parser():
    def __init__(self):
        self.pattern = [
            re.compile(r"^([0-9]+)\s+([a-zA-Z0-9_]+)\(.*"),
            re.compile(r"^()([a-zA-Z0-9_]+)\(.*"),
            re.compile(r"^\[pid\s+([0-9]+)\]\s+([a-zA-Z0-9_]+)\(.*")
        ]

    def parse_line(self, line):
        for idx, c in enumerate(self.pattern):
            m = c.match(line)
            if m is not None:
                pid = int(m.group(1)) if len(m.group(1)) > 0 else 0
                return SystemCall(idx=idx, pid=pid, func=m.group(2), line=line)
        return None


class ParseLineTest(unittest.TestCase):
    def test_parse_line(self):
        p = Parser()
        line = 'openat(AT_FDCWD, "/etc/passwd", O_RDONLY | O_CLOEXEC) = 11\n'
        syscall = p.parse_line(line)
        self.assertEqual(syscall.idx, 1)
        self.assertEqual(syscall.pid, 0)
        self.assertEqual(syscall.func, "openat")

        line = '[pid 24996] fstat(10, {st_mode=S_IFDIR|0775, st_size=4096, ...}) = 0'
        syscall = p.parse_line(line)
        self.assertEqual(syscall.idx, 2)
        self.assertEqual(syscall.pid, 24996)
        self.assertEqual(syscall.func, "fstat")

        line = '21865 access("/etc/ld.so.nohwcap", F_OK) = -1 ENOENT (No such file or directory)'
        syscall = p.parse_line(line)
        self.assertEqual(syscall.idx, 0)
        self.assertEqual(syscall.pid, 21865)
        self.assertEqual(syscall.func, "access")

        line = '21866 <... getpid resumed> )            = 21866'
        syscall = p.parse_line(line)
        self.assertIsNone(syscall)


if __name__ == '__main__':
    unittest.main()
