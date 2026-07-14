# ================================
# IMPORTS
# ================================
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.regularizers import l2
import json
import os

# ================================
# CONFIG
# ================================
IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 27

train_dir = "dataset/train"

os.makedirs("model", exist_ok=True)

# ================================
# DATA GENERATOR
# ================================
datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    zoom_range=0.2,
    horizontal_flip=True,
    validation_split=0.2
)

train = datagen.flow_from_directory(
    train_dir,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="training"
)

val = datagen.flow_from_directory(
    train_dir,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="validation"
)

# ================================
# DEBUG INFO (VERY IMPORTANT)
# ================================
print("Train samples:", train.samples)
print("Validation samples:", val.samples)
print("Classes:", train.class_indices)

# ================================
# SAVE CLASSES
# ================================
class_names = list(train.class_indices.keys())

with open("model/classes.json", "w") as f:
    json.dump(class_names, f)

# ================================
# MODEL
# ================================
base_model = EfficientNetB0(
    weights="imagenet",
    include_top=False,
    input_shape=(224,224,3)
)

# 🔥 SMART FREEZING
for layer in base_model.layers[:50]:
    layer.trainable = False

for layer in base_model.layers[50:]:
    layer.trainable = True

# ================================
# CUSTOM HEAD
# ================================
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(256, activation="relu", kernel_regularizer=l2(0.001))(x)
x = Dropout(0.35)(x)
outputs = Dense(train.num_classes, activation="softmax")(x)

model = Model(inputs=base_model.input, outputs=outputs)

# ================================
# COMPILE
# ================================
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.00007),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

# ================================
# CALLBACKS (VERY IMPORTANT)
# ================================
early_stop = EarlyStopping(
    monitor="val_loss",
    patience=4,
    restore_best_weights=True
)

reduce_lr = ReduceLROnPlateau(
    monitor="val_loss",
    factor=0.3,
    patience=2,
    min_lr=1e-6
)

# ================================
# TRAIN
# ================================
history = model.fit(
    train,
    validation_data=val,
    epochs=EPOCHS,
    callbacks=[early_stop, reduce_lr]
)

# ================================
# SAVE MODEL
# ================================
model.save("model/skin_model.h5")

print("✅ TRAINING COMPLETE")