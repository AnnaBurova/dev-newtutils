"""
Created on 2025-10

@author: NewtCode Anna Burova
"""

# from newtutils.console import error_msg
from newtutils import error_msg
import newtutils as Newt

# Test 1: just print error without stopping
print("Test 1: error_msg without stop")
error_msg("This is a test error message", stop=False)
print("This line will be printed")

print()

# Test 2: print multiline error without stopping
print("Test 2: multiline error_msg without stop")
Newt.error_msg(
    "This is a test error message",
    "This is a test error message",
    "This is a test error message",
    stop=False)
print("This line will be printed")

print()

# Test 3: error_msg with stop=True (will exit the program)
try:
    print("Test 3: error_msg with stop=True default")
    error_msg("This error will stop the program")  # This will exit
    print("This line will not be printed")
except SystemExit as e:
    print(f"Caught SystemExit with code: {e.code}")
except Exception as e:
    print(f"Caught other exception: {e}")
finally:
    print("Program continues after catching SystemExit")
