# __init__.py

"""
Lightweight Object Database Class - API.
"""

from relmgr.relationship_manager import RelationshipManager

# Version of relationship-manager package
__version__ = "2.0.0"

__all__ = ["RelationshipManager"]  # support "from relmgr import *"" syntax
