class Testdata:

    PATIENT_NAME = "AUTO"
    EMERGENCY_NAME = "EMERGENCY MEDICINE & TRAUMA"
    PEDIATRIC = "PAEDIATRICS"
    GYNOLOGY = "OBSTETRICS AND GYNAECOLOGY"


import string
import time
import random


class RandomTestData:

    patient_name = None
    department = None
    unit = None
    opd_unit_name = None

    @classmethod
    def generate_patient_name(cls, base_name):
        suffix = ''.join(
            random.choices(
                string.ascii_uppercase,
                k=3
            )
        )

        cls.patient_name = f"{base_name}{suffix}"

        return cls.patient_name

    @classmethod
    def store_department_unit(
            cls,
            department,
            unit
    ):
        cls.department = department
        cls.unit = unit

        cls.opd_unit_name = (
            f"{department.upper()}({unit.upper()})"
        )

import random

class TestDataGenerator:

    generated_mobile_numbers = set()

    @classmethod
    def generate_mobile_number(cls):
        while True:
            mobile = str(random.choice([7, 8, 9])) + ''.join(
                random.choices('0123456789', k=9)
            )

            if mobile not in cls.generated_mobile_numbers:
                cls.generated_mobile_numbers.add(mobile)
                return mobile

    generated_numbers = set()

    @classmethod
    def generate_four_digit_number(cls):
        while True:
            number = str(random.randint(1000, 9999))

            if number not in cls.generated_numbers:
                cls.generated_numbers.add(number)
                return number

    @staticmethod
    def generate_not_reg_patient_name():

        letters = string.ascii_uppercase

        timestamp = str(time.time_ns())

        random_letters = ''.join(
            random.choice(letters)
            for _ in range(8)
        )

        unique_part = ''.join(
            letters[int(x) % 26]
            for x in timestamp[-8:]
        )

        return "AUTO" + random_letters + unique_part


