import gzip
import json
import unittest


class MLModel:
    @staticmethod
    def from_file(fname):
        with gzip.open(fname, "rb") as f:
            data = json.load(f)
        seq_len = int(data["sequence_length"])
        model = MLModel(seq_len)
        model._uniq_sequences = set(data["sequences"])
        return model

    @staticmethod
    def from_sequences(sequences):
        assert(len(sequences) > 0)
        len_of_seq = [len(seq) for seq in sequences]
        first = len_of_seq[0]
        assert(all([i == first for i in len_of_seq]))
        m = MLModel(first)
        m._uniq_sequences = set([",".join(seq) for seq in sequences])
        return m

    def __init__(self, sequence_length):
        self._uniq_sequences = set()
        self._sequence_length = sequence_length

    def is_anomaly(self, sequence):
        seq = ",".join(sequence)
        return seq not in self._uniq_sequences

    def sequence_length(self):
        return self._sequence_length

# --------------------------------------------------------------------------------------------


class TestMLModel(unittest.TestCase):
    def test_from_sequences(self):
        m = MLModel.from_sequences([["a","b","c"], ["d","e","f"]])
        self.assertSetEqual(m._uniq_sequences, {"a,b,c", "d,e,f"})


if __name__ == "__main__":
    unittest.main()
