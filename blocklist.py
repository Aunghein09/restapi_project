"""
blocklist.py

This file just contains the blocklist of the JWT tokens. It will be imported by
app and the logout resource so that tokens can be added to the blocklist when the
user logs out. We don't normally use python set here. Use database of reddis for storing blocked tokens
"""

BLOCKLIST = set()
