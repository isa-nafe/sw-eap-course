from openpyxl import Workbook
import os

data_dir = os.path.join('course', 'data')
os.makedirs(data_dir, exist_ok=True)
filepath = os.path.join(data_dir, 'planner.xlsx')

wb = Workbook()
ws = wb.active
ws.title = "Course Plan"

headers = ["Week", "Topic", "Description", "Duration (hours)"]
ws.append(headers)
data = [
    (1, "Introduction to Course", "Overview of topics, grading, and schedule.", 2),
    (1, "Module 1: Basics", "Fundamental concepts and definitions.", 4),
    (2, "Module 2: Advanced Topics", "In-depth exploration of advanced concepts.", 6),
    (2, "Project Work", "Introduction to the course project.", 3),
    (3, "Module 3: Case Studies", "Analyzing real-world examples.", 5),
]
for row in data:
    ws.append(row)
wb.save(filepath)
print(f"Dummy planner saved to {filepath}")
