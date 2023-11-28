from people_generator import Person
import datetime
from random import choice, randint, uniform, sample
import json
import argparse as ap


class Payslip(object):
    def __init__(self, person: Person, reference_period: datetime, net_payment: float):
        self.person = Person(input_dict=person)
        self.reference_period = reference_period
        self.net_payment = net_payment

    def to_dict(self) -> dict:
        return {
            "person": self.person.to_dict(),
            "reference_period": self.reference_period.strftime("%m/%Y"),
            "net_payment": self.net_payment,
        }


def get_people(number_of_people: int) -> list:
    with open("resources/people.json", "r", encoding="utf-8") as f:
        people = json.load(f)
    try:
        return sample(people, number_of_people)
    except ValueError:
        print(
            f"Number of people requested ({number_of_people}) is greater than the number of people in the database ({len(people)})"
        )
        return people


def generate_payslips(people: list, num_entries: int) -> list:
    payslips = []
    for entry in range(num_entries):
        person = choice(people)
        reference_period = datetime.date(
            randint(2010, 2021), randint(1, 12), randint(1, 28)
        )
        net_payment = round(uniform(1000, 5000), 2)
        payslip = Payslip(
            person=person, reference_period=reference_period, net_payment=net_payment
        )
        payslips.append(payslip)
    return payslips


def dump_payslips_to_json(
    payslips: list, json_file: str = "data/payslips.json"
) -> None:
    payslips_dict = [payslip.to_dict() for payslip in payslips]
    # Unroll the person dict into the payslip dict
    for payslip in payslips_dict:
        for key, value in payslip["person"].items():
            payslip[key] = value
        del payslip["person"]
    # Sort the keys in the dict
    payslips_dict = [
        {key: payslip[key] for key in sorted(payslip.keys())}
        for payslip in payslips_dict
    ]
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(payslips_dict, f, ensure_ascii=False, indent=4)
    print(f"Data has been saved to {json_file}")


def main(args):
    people = get_people(args.number_of_people)
    payslips = generate_payslips(people, args.number_of_payslips)
    dump_payslips_to_json(payslips, args.dest)


if __name__ == "__main__":
    ap = ap.ArgumentParser()
    ap.add_argument(
        "-n",
        "--number-of-payslips",
        type=int,
        default=1000,
        help="Number of payslips to generate",
    )
    ap.add_argument(
        "-p",
        "--number-of-people",
        type=int,
        default=50,
        help="Number of people to use",
    )
    ap.add_argument(
        "-d",
        "--dest",
        type=str,
        default="resources/payslips.json",
        help="Destination file",
    )
    args = ap.parse_args()
    main(args)
