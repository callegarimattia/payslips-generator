from random import randint, choice, sample
import json
from codicefiscale import codicefiscale
import datetime
import argparse


class Person(object):
    def __init__(
        self,
        first_name: str = None,
        last_name: str = None,
        birth_date: datetime = None,
        employment_date: datetime = None,
        birth_place: str = None,
        gender: str = None,
        input_dict: dict = None,
    ):
        if input_dict:
            self.first_name = input_dict["first_name"]
            self.last_name = input_dict["last_name"]
            self.birth_date = datetime.datetime.strptime(
                input_dict["birth_date"], "%d/%m/%Y"
            )
            self.birth_place = input_dict["birth_place"]
            self.employment_date = datetime.datetime.strptime(
                input_dict["employment_date"], "%d/%m/%Y"
            )
            self.gender = input_dict["gender"]
            self.tax_id = input_dict["tax_id"]
        else:
            self.first_name = first_name
            self.last_name = last_name
            self.birth_date = birth_date
            self.birth_place = birth_place
            self.employment_date = employment_date
            self.gender = gender
            self.tax_id = self._get_codice_fiscale()

    def _get_codice_fiscale(self):
        return codicefiscale.encode(
            lastname=self.last_name,
            firstname=self.first_name,
            gender=self.gender,
            birthdate=self.birth_date.strftime("%d/%m/%Y"),
            birthplace=self.birth_place,
        )

    def to_dict(self) -> dict:
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birth_date": self.birth_date.strftime("%d/%m/%Y"),
            "birth_place": self.birth_place,
            "employment_date": self.employment_date.strftime("%d/%m/%Y"),
            "gender": self.gender,
            "tax_id": self.tax_id,
        }


def load_data_from_json(json_file: str = "resources/it_data.json") -> dict:
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def generate_people(num_entries: int, json_file) -> list:
    data = load_data_from_json(json_file=json_file)
    people = set()
    for entry in range(num_entries):
        first_name = choice(data["first_names"])
        last_name = choice(data["last_names"])
        birth_date = datetime.date(randint(1950, 2003), randint(1, 12), randint(1, 28))
        employment_date = datetime.date(
            randint(birth_date.year + 18, 2023), randint(1, 12), randint(1, 28)
        )
        gender = choice(["M", "F"])
        birth_place = choice(data["cities"])
        person = Person(
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
            birth_place=birth_place,
            employment_date=employment_date,
            gender=gender,
        )
        people.add(person)

    return list(people)


def dump_people_to_json(people: list(), dest: str) -> None:
    # Save the data to a JSON file
    with open(dest, "w", encoding="utf-8") as json_file:
        json.dump(
            [person.to_dict() for person in people],
            json_file,
            indent=4,
            ensure_ascii=False,
        )
    print(f"Data has been saved to {dest}")


def get_people(number_of_people: int, json_file: str = "resources/people.json") -> list:
    with open(json_file, "r", encoding="utf-8") as f:
        people = json.load(f)
    try:
        return sample(people, number_of_people)
    except ValueError:
        print(
            f"Number of people requested ({number_of_people}) is greater than the number of people in the database ({len(people)})"
        )
        return people


def main(args):
    people = generate_people(json_file=args.input_data, num_entries=args.num_entries)
    dump_people_to_json(people=people, dest=args.dest)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-n",
        "--num_entries",
        default=1000,
        help="Number of entries to generate (Default is 100)",
        type=int,
    )
    ap.add_argument(
        "-i",
        "--input_data",
        default="resources/it_data.json",
        help="JSON file containing the data to generate the people",
        type=str,
    )
    ap.add_argument(
        "-d",
        "--dest",
        default="resources/people.json",
        help="Destination file",
        type=str,
    )
    main(ap.parse_args())
