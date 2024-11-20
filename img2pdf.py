from reportlab.pdfgen import canvas
from PIL import Image
import os
import shutil

current_directory = os.path.dirname(os.path.realpath(__file__))

def image_to_pdf(image_paths, pdf_path):
    new_canvas = canvas.Canvas(pdf_path)

    for i, image_path in enumerate(image_paths):
        image = Image.open(image_path)
        print(image_path)
        new_canvas.setPageSize((image.width, image.height))
        new_canvas.drawInlineImage(image, 0, 0, width = image.width, height=image.height)
        if i < len(image_paths) - 1:
            new_canvas.showPage()

    new_canvas.save()

def list_files(path):
    entries = os.listdir(path)
    return [os.path.join(path, entry) for entry in entries if os.path.isfile(os.path.join(path, entry))]

def list_subdirectories(path):
    entries = os.listdir(path)
    return [os.path.join(path, entry) for entry in entries if os.path.isdir(os.path.join(path, entry))]



def process_all():

    working_path = os.path.join(current_directory, "work")
    items = list_subdirectories(working_path)

    print(items)

    for item in items:
        image_paths = list_files(item)
        pdf_path = item + ".pdf"
        print("Processing " + item)
        image_to_pdf(image_paths, pdf_path)

        print(item)

        n = input()

        shutil.rmtree(item)
