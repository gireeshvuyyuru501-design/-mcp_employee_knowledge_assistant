"""
Simple local test file.
This does not start MCP. It directly imports the helper functions for learning.
"""

from server import find_employee, get_employee_email, list_employees, search_department

print("All employees:")
print(list_employees())

print("\nFind Ravi:")
print(find_employee("Ravi"))

print("\nIT Department:")
print(search_department("IT"))

print("\nAsha Email:")
print(get_employee_email("Asha"))
