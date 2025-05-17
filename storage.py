import csv
from typing import List, TypeVar, Type
from pathlib import Path
import os

T = TypeVar('T')

class Storage:
    @staticmethod
    def read_csv(file_path: str, model_class: Type[T]) -> List[T]:
        if not Path(file_path).exists():
            return []
            
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            return [model_class(**row) for row in reader]

    @staticmethod
    def write_csv(file_path: str, data: List[object]):
        if not data:
            return
            
        fieldnames = list(data[0].__dict__.keys())
        with open(file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for item in data:
                writer.writerow(item.__dict__)