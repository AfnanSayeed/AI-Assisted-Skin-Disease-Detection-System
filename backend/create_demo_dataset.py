from PIL import Image, ImageDraw
import os
import random

# ---------------- CONFIG ----------------
dataset_path = "backend/dataset_demo"
classes = ["Nevus", "Melanoma", "BasalCellCarcinoma", "ActinicKeratosis"]
images_per_class = 20
image_size = (224, 224)  # standard CNN input size

# ---------------- CREATE FOLDERS ----------------
os.makedirs(dataset_path, exist_ok=True)
for cls in classes:
    os.makedirs(os.path.join(dataset_path, cls), exist_ok=True)

# ---------------- GENERATE SYNTHETIC IMAGES ----------------
print("Generating synthetic dataset...")
for cls in classes:
    for i in range(images_per_class):
        # create blank white image
        img = Image.new("RGB", image_size, "white")
        draw = ImageDraw.Draw(img)

        # draw random colored ellipse
        x0, y0 = random.randint(10, 150), random.randint(10, 150)
        x1, y1 = x0 + random.randint(30, 70), y0 + random.randint(30, 70)
        draw.ellipse([x0, y0, x1, y1], fill=(random.randint(100,255), 0, 0))

        # save image
        img.save(os.path.join(dataset_path, cls, f"{cls}_{i}.png"))

print(f"Synthetic dataset created at '{dataset_path}' with {images_per_class} images per class.")
