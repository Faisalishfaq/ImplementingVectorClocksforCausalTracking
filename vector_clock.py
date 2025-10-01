# vector_clock.py

class VectorClock:
    def __init__(self, node_id=None, clock=None):
        self.node_id = node_id
        self.clock = dict(clock) if clock else {}

    def increment(self, node_id=None):
        nid = node_id or self.node_id
        if nid is None:
            raise ValueError("node_id required to increment")
        self.clock[nid] = self.clock.get(nid, 0) + 1
        return self.clock

    def update(self, other):
        other_clock = other.clock if isinstance(other, VectorClock) else other
        for k, v in (other_clock or {}).items():
            self.clock[k] = max(self.clock.get(k, 0), v)
        return self.clock

    def compare(self, other):
        other_clock = other.clock if isinstance(other, VectorClock) else other or {}
        keys = set(self.clock.keys()) | set(other_clock.keys())
        less = greater = False
        for k in keys:
            a, b = self.clock.get(k, 0), other_clock.get(k, 0)
            if a < b: less = True
            elif a > b: greater = True
        if not less and not greater: return "equal"
        if less and not greater: return "happens-before"
        if greater and not less: return "happens-after"
        return "concurrent"

    def to_dict(self):
        return dict(self.clock)

    def __repr__(self):
        return f"VectorClock({self.clock})"
