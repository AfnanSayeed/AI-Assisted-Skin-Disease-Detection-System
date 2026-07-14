import os
import shutil
import pandas as pd
from sklearn.model_selection import train_test_split

RAW_DIR = "dataset_raw"
IMG_DIR1 = os.path.join(RAW_DIR, "HAM10000_images_part_1")
IMG_DIR2 = os.path.join(RAW_DIR, "HAM10000_images_part_2")
META_FILE = os.path.join(RAW_DIR, "HAM10000_metadata.csv")

OUT_DIR = "dataset"
TRAIN_DIR = os.path.join(OUT_DIR, "train")
VAL_DIR = os.path.join(OUT_DIR, "val")

CLASSES = {
    "nv": "Normal",
    "mel": "Melanoma",
    "bkl": "Psoriasis",
    "akiec": "Eczema",
    "bcc": "Acne"
}

# -------------------------
# CLEAN OLD DATASET
# -------------------------
if os.path.exists(OUT_DIR):
    shutil.rmtree(OUT_DIR)

for split in [TRAIN_DIR, VAL_DIR]:
    for c in CLASSES.values():
        os.makedirs(os.path.join(split, c), exist_ok=True)

# -------------------------
# LOAD CSV
# -------------------------
df = pd.read_csv(META_FILE)
df = df[df["dx"].isin(CLASSES.keys())]

train_df, val_df = train_test_split(
    df,
    test_size=0.2,
    stratify=df["dx"],
    random_state=42
)

def copy_images(dataframe, target_root):
    copied = 0
    for _, row in dataframe.iterrows():
        img = row["image_id"] + ".jpg"
        label = CLASSES[row["dx"]]

        src1 = os.path.join(IMG_DIR1, img)
        src2 = os.path.join(IMG_DIR2, img)

        if os.path.exists(src1):
            src = src1
        elif os.path.exists(src2):
            src = src2
        else:
            continue

        dst = os.path.join(target_root, label, img)
        shutil.copy(src, dst)
        copied += 1
    return copied

train_count = copy_images(train_df, TRAIN_DIR)
val_count = copy_images(val_df, VAL_DIR)

print(f"✅ Training images: {train_count}")
print(f"✅ Validation images: {val_count}")
print("✅ Dataset prepared successfully!")
