import json
from PIL import Image, ImageDraw, ImageFont
import argparse
from random import sample
import os
# Generate payslips from a png template
# Generate annotations with bboxs and labels

# Get the backfilled data from the payslips
# Generate a json file with the data
# Generate a json file with the annotations


def load_data_from_json(json_file: str = "resources/payslips.json") -> dict:
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def extract_payslips_from_data(data: dict) -> list:
    payslips = []
    for payslip in data:
        payslips.append(payslip)
    return payslips


def load_template(
    template_file: str = "resources/templates/template.jpg",
    annotations_file: str = "resources/templates/annotations.json",
) -> (Image, dict):
    with open(annotations_file, "r", encoding="utf-8") as f:
        template = Image.open(template_file)
        annotations = json.load(f)
    return template, annotations


def paste(annotations: dict, template: Image, payslip: dict) -> (Image, dict):
    # Clone the template
    template_clone = template.copy()
    font = ImageFont.load_default(size=16)
    tokens = []
    labels = []
    bboxs = []
    for entry in annotations:
        # Get the bbox and label from the annotation
        bbox = entry["bbox"]
        label = entry["label"]
        # Get the entry from the payslip
        try:
            value = payslip[label]
        except KeyError:
            print(f"Label {label} not found!")
            continue
        # Paste the entry on the template
        ImageDraw.Draw(template_clone).text(
            xy=bbox[:2],
            text=str(value),
            font=font,
            fill=(0, 0, 0),
        )
        tokens.append(str(value))
        labels.append(label)
        bbox = [float(x / 1000) for x in bbox]
        bboxs.append(bbox)
    # Save the annotation
    ner_annotation = {
        "tokens": tokens,
        "labels": labels,
        "bbox": bboxs,
    }
    return template_clone, ner_annotation


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "--number_of_payslips",
        "-n",
        type=int,
        default=100,
        help="Number of payslips to generate",
    )
    num = argparser.parse_args().number_of_payslips
    data = load_data_from_json()
    payslips = extract_payslips_from_data(data)
    template, annotations = load_template()
    if not os.path.exists("dataset/images"):
        os.makedirs("dataset/images")
    if not os.path.exists("dataset/annotations"):
        os.makedirs("dataset/annotations")
    index = 0
    for payslip in sample(payslips, num):
        try:
            new_payslip, new_annotation = paste(
                annotations["annotations"], template, payslip
            )
            new_payslip.save("dataset/images/" + str(index).zfill(4) + ".png")
            with open("dataset/annotations/" + str(index).zfill(4) + ".json", "w") as f:
                json.dump(new_annotation, f)

        except IndexError:
            print(f"Index {index} not found in annotations")
            continue
        index += 1
