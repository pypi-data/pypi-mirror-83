from django.test import TestCase
from .Parser import  parse_or,parse_and,Parse


class TestParser(TestCase):
    def test_all(self):
        pass
    def test_basic(self):
        Parse({"status":"Completed"})

    def test_or(self):
        d = {"or": {
            "status": "Completed",
            "ordered_by_id": 2
        }}
        print (parse_or(d))
