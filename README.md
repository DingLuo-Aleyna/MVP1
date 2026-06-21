# AML MVP local setup

## Dataset

`SAML-D.csv` is about 950 MB and is intentionally excluded from Git. After
cloning this repository, place the dataset in the project root before starting
the app. Do not commit API keys, customer data, or other sensitive data.

## Start on macOS

Open Terminal and run:

```bash
cd "/Users/caoyuhan/Desktop/MVP2"
chmod +x run.sh
./run.sh
```

The launcher first uses an existing compatible Python environment (including
Anaconda). If none is available, it creates `.venv` and installs the Python
dependencies. Streamlit then opens at <http://localhost:8501>.

By default, the app loads all rows from `SAML-D.csv`. To use a smaller sample:

```bash
AML_MAX_ROWS=1000000 ./run.sh
```

To explicitly load all 9.5 million rows (requires substantially more memory
and time):

```bash
AML_MAX_ROWS=0 ./run.sh
```

## Train once, deploy for inference

Run the full training job locally once:

```bash
/opt/anaconda3/bin/python train_model.py
```

This creates `aml_model_bundle.joblib`. After that, `./run.sh` loads the model
bundle and no longer reads or trains on `SAML-D.csv`. Commit the bundle with the
application code before deploying:

```bash
git add aml_model_bundle.joblib train_model.py app1.1.py requirements.txt
git commit -m "Add pre-trained AML model bundle"
git push
```

If the bundle is larger than GitHub's normal file limit, store it with Git LFS
or in cloud object storage instead of regular Git.
