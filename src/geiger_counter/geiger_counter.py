from collections import deque

CPM_LEN = 60
CPH_LEN = 3600

class GeigerCounter:
    def __init__(self):
        self._latest_cps = 0
        self._latest_cpm = 0
        self._latest_cph = 0
        self._cpm_buffer = deque(maxlen=CPM_LEN)
        self._cph_buffer = deque(maxlen=CPH_LEN)
    
    def is_empty(self):
        return len(self._cpm_buffer) == 0
    
    def add_cps(self, cps: int):
        self._latest_cps = cps
        self._cpm_buffer.append(cps)
        self._cph_buffer.append(cps)
        self._latest_cpm = sum(self._cpm_buffer)
        self._latest_cph = sum(self._cph_buffer)
    
    def get_data(self):
        return {"cps": self._latest_cps, "cpm": self._latest_cpm, "cph": self._latest_cph}

    def get_cph_buffer(self, count: int = None):
        buf_list = list(self._cph_buffer)
        # If the requested count is greater than or equal to the number of items, return all items.
        if count >= len(buf_list) or count is None:
            return buf_list
        # Otherwise, return only the last `count` items.
        return buf_list[-count:]
