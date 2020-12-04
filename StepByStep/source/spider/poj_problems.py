import requests
import time
from source.models import Problem, Source


def poj_problems():
    # TODO
    resp = requests.get("http://poj.org/problemlist?volume=1")
