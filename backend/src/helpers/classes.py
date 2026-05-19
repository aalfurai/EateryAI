class NumRange:
    """Simple container class for storing numerical range for filters"""
    def __init__(self, min, max):
        self.min = min
        self.max = max

    @property
    def get_min(self):
        return self.min

    @property
    def get_max(self):
        return self.max

    def is_max_none(self):
        return self.max == None

    def is_min_none(self):
        return self.min == None