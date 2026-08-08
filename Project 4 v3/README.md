# Project 4 v3 — Bahraini Banknote Classification

Three neural networks (Sequential API, Functional API, CNN) that tell apart the
five Bahraini banknotes: 0.5, 1, 5, 10 and 20 BHD.

## Results

| Model | Parameters | Test accuracy |
|---|---|---|
| Sequential | 6,265,305 | 55.1% |
| Functional | 6,265,305 | 49.4% |
| **CNN** | **683,845** | **84.0%** |

On `realtest.zip` — 138 photographs of banknotes that are **not** in the
training data at all — the CNN gets **92.8%**:

| Class | precision | recall | f1 |
|---|---|---|---|
| 0.5 BHD | 0.92 | 0.82 | 0.87 |
| 1 BHD | 0.97 | 0.91 | 0.94 |
| 5 BHD | 1.00 | 1.00 | 1.00 |
| 10 BHD | 1.00 | 1.00 | 1.00 |
| 20 BHD | 0.81 | 0.94 | 0.87 |

The CNN beats both Dense models using **nine times fewer parameters**. `Flatten`
throws away where things are in the picture; `Conv2D` keeps it.

## The data

`dataset_clean.zip` — 1,556 photographs:

- my own photos of Bahraini banknotes
- three public datasets from Roboflow (all CC BY 4.0), which are photos of
  **other people's** banknotes:
  - https://universe.roboflow.com/mohameds-workspace-wg0dv/bahraini-currency
  - https://universe.roboflow.com/ga-asqfm/bahrain_currency
  - https://universe.roboflow.com/aymans-workplace/currency-detector-piulz

Removed from those datasets: coins (50 and 100 fils), Indian rupees (not
Bahraini), and images labelled only "currency" with no denomination.

## Avoiding data leakage

This mattered more than any change to the models.

Leakage is when nearly the same picture ends up in both training and testing.
The model then looks accurate but has really just memorised the picture. I
found it three times:

1. **Augmented copies.** My original dataset had 757 pairs of pictures more
   than 95% identical.
2. **Several crops of one photo.** Cropping one photo many times and splitting
   randomly puts copies on both sides. This alone pushed a test score up to 92%
   when the honest number was much lower.
3. **The public datasets overlap each other.** The same photo appears in more
   than one of them under a different web address, so a photo I had "held out"
   was sitting in the training data through another dataset.

Fix: compare every picture to every other one and delete near copies before
splitting. After cleaning, no two pictures are more than 93% similar, and no
training picture is that close to any test picture.

## Files

| File | |
|---|---|
| `Currency_three_models.ipynb` | the three models |
| `currency_model.keras` | the trained CNN |
| `app.py` | Streamlit app (upload or camera) |
| `dataset_clean.zip` | training data |
| `realtest.zip` | held-out photos, never trained on |

## Running it

Notebook: open in Colab, run all, upload `dataset_clean.zip` when asked.

App: `streamlit run app.py` (needs `currency_model.keras` in the same folder).

## What I would do next

0.5 BHD and 20 BHD are the weakest at 0.87. Both would improve with more
photographs — accuracy tracked photo count almost exactly across every
experiment I ran.
