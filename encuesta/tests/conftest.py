import sys
from pathlib import Path

ENCUESTA_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ENCUESTA_DIR))

import pytest  # noqa: E402

from motor import db  # noqa: E402


@pytest.fixture
def conn(tmp_path):
    return db.connect(tmp_path / "test.db")
