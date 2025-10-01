# vector_clock.py
"""
Vector Clock Implementation
---------------------------
This module provides a VectorClock class which supports:
1. increment(node_id) – increment local counter
2. update(other_clock) – merge with another vector clock
3. compare(other_clock) – determine happens-before, concurrent, or equal
"""

class VectorClock:
    def __init__(self, node_id):
        self.node_id = node_id
        self.clock = {node_id: 0}

    def increment(self, node_id=None):
        """Increment local counter (default: this node)."""
        if node_id is None:
            node_id = self.node_id
        self.clock[node_id] = self.clock.get(node_id, 0) + 1

    def update(self, other_clock):
        """Merge this vector clock with another one."""
        for node, value in other_clock.items():
            self.clock[node] = max(self.clock.get(node, 0), value)

    def compare(self, other_clock):
        """
        Compare this vector clock with another.
        Returns: "happens-before (→)", "happens-after (←)", "concurrent (‖)", or "equal (=)"
        """
        less, greater = False, False
        for node in set(self.clock) | set(other_clock):
            self_val = self.clock.get(node, 0)
            other_val = other_clock.get(node, 0)
            if self_val < other_val:
                less = True
            elif self_val > other_val:
                greater = True

        if less and not greater:
            return "happens-before (→)"
        elif greater and not less:
            return "happens-after (←)"
        elif greater and less:
            return "concurrent (‖)"
        else:
            return "equal (=)"

    def to_dict(self):
        return dict(self.clock)

    def __repr__(self):
        return str(self.clock)
