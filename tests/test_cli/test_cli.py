from pathlib import Path

from dacoromanica_downloader import cli


def test_cli_passes_parsed_arguments_to_application(monkeypatch, tmp_path):
    source = tmp_path / "urls.txt"
    destination = tmp_path / "downloads"
    expected_urls = [
        "https://example.com/collection/1",
        "https://example.com/collection/2",
    ]

    received_arguments: dict[str, object] = {}

    def fake_get_starting_urls(urls_file_path: Path) -> list[str]:
        received_arguments["source"] = urls_file_path
        return expected_urls

    def fake_run_dacoromanica_downloader(
        *,
        starting_urls: list[str],
        destination_folder: Path,
    ) -> None:
        received_arguments["starting_urls"] = starting_urls
        received_arguments["destination"] = destination_folder

    monkeypatch.setattr(cli, "get_starting_urls", fake_get_starting_urls)
    monkeypatch.setattr(
        cli, "run_dacoromanica_downloader", fake_run_dacoromanica_downloader
    )

    exit_code = cli.main(
        [
            "--source",
            str(source),
            "--destination",
            str(destination),
        ]
    )

    assert exit_code == 0
    assert received_arguments == {
        "source": source,
        "starting_urls": expected_urls,
        "destination": destination,
    }


def test_cli_returns_error_when_source_file_does_not_exist(tmp_path, capsys):
    missing_source = tmp_path / "missing.txt"

    exit_code = cli.main(["--source", str(missing_source)])

    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Error:" in captured.err
    assert str(missing_source) in captured.err


def test_cli_uses_default_paths(monkeypatch):
    received_arguments: dict[str, object] = {}

    def fake_get_starting_urls(
        urls_file_path: Path,
    ) -> list[str]:
        received_arguments["source"] = urls_file_path
        return ["https://example.com/collection"]

    def fake_run_dacoromanica_downloader(
        *,
        starting_urls: list[str],
        destination_folder: Path,
    ) -> None:
        received_arguments["destination"] = destination_folder

    monkeypatch.setattr(cli, "get_starting_urls", fake_get_starting_urls)
    monkeypatch.setattr(
        cli, "run_dacoromanica_downloader", fake_run_dacoromanica_downloader
    )

    exit_code = cli.main([])

    assert exit_code == 0
    assert received_arguments["source"] == Path("starting_urls.txt")
    assert received_arguments["destination"] == Path("downloaded_files")
