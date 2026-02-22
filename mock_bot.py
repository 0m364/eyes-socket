#!/usr/bin/env python3
import sys

# Join all arguments into a single string
prompt = " ".join(sys.argv[1:])
# If no arguments, try reading from stdin
if not prompt:
    try:
        # Check if stdin has content
        if not sys.stdin.isatty():
             prompt = sys.stdin.read().strip()
    except Exception:
        pass

print(f"Mock Response: You said '{prompt}'")
