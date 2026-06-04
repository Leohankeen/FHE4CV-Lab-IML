# Labels CSV Format

Use this format when training/exporting a plaintext linear model with real
labels:

```csv
image,label
000001-1.jpg,1
000001-10.jpg,0
```

Rules:

- `image`: file name only, matching an image in `data/chestxray_sample/` or the
  selected `--data-dir`.
- `label`: integer class, currently `0` or `1`.
- Every image in `--data-dir` must have a label row.

Example command:

```powershell
python scripts/train_plaintext_linear_model.py --labels-csv data/chestxray_sample_labels_demo.csv --output-model models/triage_linear_model.json
```

The included `data/chestxray_sample_labels_demo.csv` is deterministic demo data,
not medical ground truth.
