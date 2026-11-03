import subprocess

import pytest

import converter
from converter import WordToPDFConverter, unique_output_path


@pytest.fixture
def docx(tmp_path):
    path = tmp_path / "rapor.docx"
    path.write_bytes(b"fake")
    return path


def fake_backend(content=b"%PDF"):
    def backend(source, target):
        with open(target, "wb") as f:
            f.write(content)
    return backend


def failing_backend(message):
    def backend(source, target):
        raise RuntimeError(message)
    return backend


def test_unique_output_path(tmp_path):
    assert unique_output_path(tmp_path, "rapor") == tmp_path / "rapor.pdf"

    (tmp_path / "rapor.pdf").write_bytes(b"")
    (tmp_path / "rapor_1.pdf").write_bytes(b"")

    assert unique_output_path(tmp_path, "rapor") == tmp_path / "rapor_2.pdf"


def test_missing_input_fails(tmp_path):
    app = WordToPDFConverter()

    assert app.convert(str(tmp_path / "yok.docx"), str(tmp_path / "yok.pdf")) is False
    assert "bulunamadı" in app.last_error


def test_word_is_tried_first(docx, tmp_path, monkeypatch):
    calls = []
    app = WordToPDFConverter()
    monkeypatch.setattr(app, "backends", (
        ("Word", lambda s, t: (calls.append("word"), fake_backend()(s, t))),
        ("LibreOffice", lambda s, t: calls.append("libreoffice")),
    ))

    assert app.convert(str(docx), str(tmp_path / "out" / "rapor.pdf")) is True
    assert calls == ["word"]


def test_falls_back_to_libreoffice(docx, tmp_path, monkeypatch):
    app = WordToPDFConverter()
    monkeypatch.setattr(app, "backends", (
        ("Word", failing_backend("Word yok")),
        ("LibreOffice", fake_backend()),
    ))

    assert app.convert(str(docx), str(tmp_path / "rapor.pdf")) is True
    assert app.last_error is None


def test_all_backends_failing_reports_each(docx, tmp_path, monkeypatch):
    app = WordToPDFConverter()
    monkeypatch.setattr(app, "backends", (
        ("Word", failing_backend("Word yok")),
        ("LibreOffice", failing_backend("LibreOffice bulunamadı")),
    ))

    assert app.convert(str(docx), str(tmp_path / "rapor.pdf")) is False
    assert "Word yok" in app.last_error
    assert "LibreOffice bulunamadı" in app.last_error


def test_libreoffice_command_and_move(docx, tmp_path, monkeypatch):
    commands = []

    def fake_run(command, **kwargs):
        commands.append(command)
        outdir = command[command.index("--outdir") + 1]
        (converter.Path(outdir) / "rapor.pdf").write_bytes(b"%PDF")
        return subprocess.CompletedProcess(command, 0)

    monkeypatch.setattr(converter, "find_libreoffice", lambda: "soffice")
    monkeypatch.setattr(converter.subprocess, "run", fake_run)
    target = tmp_path / "sonuc.pdf"

    converter.convert_with_libreoffice(str(docx), str(target))

    assert commands[0][:4] == ["soffice", "--headless", "--convert-to", "pdf"]
    assert target.read_bytes() == b"%PDF"


def test_libreoffice_missing(docx, tmp_path, monkeypatch):
    monkeypatch.setattr(converter, "find_libreoffice", lambda: None)

    with pytest.raises(RuntimeError, match="LibreOffice"):
        converter.convert_with_libreoffice(str(docx), str(tmp_path / "x.pdf"))
