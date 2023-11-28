import matplotlib.pyplot as plt
import matplotlib.patches as patches
import json
import os


def draw_bbox(image_path, color):
    # Open the image using Matplotlib
    img = plt.imread(image_path)
    fig, ax = plt.subplots(1)
    ax.imshow(img)

    with open("resources/templates/annotations.json") as f:
        annotations = json.load(f)

    for annotation in annotations["annotations"]:
        # Extract bounding box coordinates
        x0, y0, x1, y1 = annotation["bbox"]
        label = annotation["label"]

        # Create a Rectangle patch
        rect = patches.Rectangle(
            (x0, y0),
            x1 - x0,
            y1 - y0,
            linewidth=2,
            edgecolor=color[label],
            facecolor="none",
        )

        # Add the Rectangle patch to the Axes
        ax.add_patch(rect)

        # Add label text
        font_size = 10
        ax.text(x0, y0 - font_size, label, color=color[label], fontsize=font_size)

    # Display the plot
    plt.ion()
    plt.show()
    # Wait for the user to continue
    plt.waitforbuttonpress()
    plt.close()
    plt.ioff()


# Use color names or RGB values
# map color names to labels
color_map = {
    "first_name": "red",
    "last_name": "blue",
    "tax_id": "green",
    "net_payment": "yellow",
}
folder = "dataset/images"
for images in os.listdir(folder):
    image_path = os.path.join(folder, images)
    draw_bbox(image_path, color_map)
