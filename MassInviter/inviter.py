import multiprocessing
from . import Inviter

# not used

def run(self,organisation_name:str,organisation_owner_username:str,organisation_owner_password:str):
    processes_count = multiprocessing.cpu_count()

    search_results = []

    for i in range(processes_count):
        search_results[len(search_results) / i : len(search_results) / processes_count * i ]