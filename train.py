import pandas as pd
from datasets import load_dataset
from fastai.text.all import *
import torch
import torch.serialization
from fastcore.foundation import L

# Force CPU usage to avoid MPS issues
import os
os.environ['CUDA_VISIBLE_DEVICES'] = ''
torch.backends.mps.is_available = lambda: False

# Load dataset from Hugging Face Parquet file
df = pd.read_parquet("hf://datasets/boltuix/emotions-dataset/emotions_dataset.parquet")

# Convert labels to string
df['Label'] = df['Label'].astype(str)

# Load into DataLoaders
dls = TextDataLoaders.from_df(
    df,
    text_col='Sentence',
    label_col='Label',
    valid_pct=0.2,
    seed=42,
    bs=32  # Reduced batch size for CPU
)

# Define ULMFiT learner
learn = text_classifier_learner(
    dls,
    AWD_LSTM,
    drop_mult=0.7, # dropout to avoid overfitting
    metrics=[accuracy, F1Score(average="macro")]
)

# Find learning rate
lr_result = learn.lr_find()

# Use suggested learning rate
print(f"Suggested LR (valley): {lr_result.valley:.2e}")

# Fine-tune the model
learn.fine_tune(6, base_lr=lr_result.valley)

# Export the trained model
learn.export('emotion_classifier.pkl')

print("Model training complete and saved as emotion_classifier.pkl")
