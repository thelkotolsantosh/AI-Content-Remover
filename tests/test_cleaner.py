from pathlib import Path
import runpy

import pytest

Cleaner = runpy.run_path(str(Path(__file__).parents[1] / 'REMOVER.PY'))['GitHubRepoCleaner']


def test_python_source_is_copied_without_changing_indentation(tmp_path):
    source = tmp_path / 'source'
    source.mkdir()
    code = 'def sample():\n    if True:\n        return "robust"\n'
    (source / 'sample.py').write_text(code)
    output = tmp_path / 'output'
    Cleaner(source, output).scan_and_clean()
    assert (output / 'sample.py').read_text() == code


def test_output_inside_source_is_rejected(tmp_path):
    with pytest.raises(ValueError):
        Cleaner(tmp_path, tmp_path / 'output').scan_and_clean()


def test_markdown_code_examples_are_preserved(tmp_path):
    source = tmp_path / 'source'
    source.mkdir()
    example = '```python\ndef sample():\n    return "robust"\n```'
    (source / 'README.md').write_text('A robust example.\n\n' + example)
    output = tmp_path / 'output'
    Cleaner(source, output).scan_and_clean()
    cleaned = (output / 'README.md').read_text()
    assert example in cleaned
    assert 'A strong example.' in cleaned
