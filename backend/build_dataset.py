import os, csv, shutil, random

RAW_PATH = "dataset_raw"
OUT_PATH = "dataset"

IMG1 = os.path.join(RAW_PATH, "HAM10000_images_part1")
IMG2 = os.path.join(RAW_PATH, "HAM10000_images_part2")
META = os.path.join(RAW_PATH, "HAM10000_metadata.csv")

# HAM10000 remapped to 5 diseases
CLASSES = {
    "nv": "Normal Skin",
    "mel": "Melanoma",
    "bkl": "Acne",
    "bcc": "Psoriasis",
    "akiec": "Eczema"
}

SPLIT = 0.8

for split in ["train","val"]:
    for cls in CLASSES.values():
        os.makedirs(os.path.join(OUT_PATH,split,cls),exist_ok=True)

with open(META) as f:
    rows = list(csv.DictReader(f))

random.shuffle(rows)

count = 0

for row in rows:
    label = row["dx"]
    if label not in CLASSES:
        continue

    img = row["image_id"] + ".jpg"

    src = os.path.join(IMG1,img)
    if not os.path.exists(src):
        src = os.path.join(IMG2,img)

    if not os.path.exists(src):
        continue

    folder = "train" if random.random() < SPLIT else "val"
    dest = os.path.join(
        OUT_PATH,
        folder,
        CLASSES[label],
        img
    )

    shutil.copy(src,dest)
    count += 1

print("✅ Images copied:", count)
