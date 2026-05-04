from pathlib import Path

import pytest

from scripts.load_data import load_data


def test_loader_raises_for_missing_file():
    missing_path = Path("does-not-exist.csv")

    with pytest.raises(FileNotFoundError):
        load_data(missing_path, missing_path)
