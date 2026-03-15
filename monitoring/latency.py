import time


class LatencyTracker:

    def __init__(self):
        self.times = {}

    def start(self, key):
        self.times[key] = {"start": time.time()}

    def end(self, key):
        self.times[key]["end"] = time.time()

    def get_latency(self):

        results = {}

        for k, v in self.times.items():
            duration = v["end"] - v["start"]
            results[k] = round(duration, 3)

        total = sum(results.values())
        results["total"] = round(total, 3)

        return results