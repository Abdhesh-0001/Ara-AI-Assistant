import json
import os

class QuizTracker:
    def __init__(self, filename="quiz_scores.json"):
        self.filename = filename
        self.scores = {}
        self.load_scores()
    
    def load_scores(self):
        if os.path.exists(self.filename):
            with open(self.filename) as f:
                self.scores = json.load(f)
    
    def add_score(self, student, score):
        self.scores[student] = score
        self.save_scores()
    
    def save_scores(self):
        with open(self.filename, "w") as f:
            json.dump(self.scores, f)
    
    def get_average(self):
        total = sum(self.scores.values())
        avg = total / len(self.scores)
        return avg
    
    def get_passed(self):
        passed = [s for s in self.scores if self.scores[s] >= 50]
        return passed

# Usage
tracker = QuizTracker()
tracker.add_score("Alice", 85)
tracker.add_score("Bob", 45)
tracker.add_score("Charlie", 92)

print(f"Average: {tracker.get_average()}")
print(f"Passed: {tracker.get_passed()}")