"""Train the AML model once and write aml_model_bundle.joblib."""

import argparse
import os
from pathlib import Path

from streamlit.testing.v1 import AppTest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--max-rows",
        type=int,
        default=0,
        help="Rows to train on; 0 loads the complete dataset (default).",
    )
    parser.add_argument("--timeout", type=int, default=7200)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent / "aml_model_bundle.joblib",
    )
    args = parser.parse_args()

    os.environ["AML_TRAIN_MODEL"] = "1"
    os.environ["AML_MAX_ROWS"] = str(args.max_rows)
    os.environ["AML_MODEL_BUNDLE_PATH"] = str(args.output.resolve())

    app_path = Path(__file__).resolve().parent / "app1.1.py"
    app = AppTest.from_file(str(app_path))
    app.run(timeout=args.timeout)

    if app.exception:
        messages = "\n".join(str(exception.value) for exception in app.exception)
        raise RuntimeError(f"Training failed:\n{messages}")

    bundle_path = args.output.resolve()
    if not bundle_path.exists():
        raise RuntimeError("Training completed without creating the model bundle.")

    size_mb = bundle_path.stat().st_size / (1024 * 1024)
    print(f"Model bundle created: {bundle_path} ({size_mb:.1f} MB)")


if __name__ == "__main__":
    main()
