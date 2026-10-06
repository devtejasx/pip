from __future__ import annotations

import email.parser
import logging

import pytest

from pip._internal.commands.show import _PackageInfo, print_results


def _package_info(metadata_version: str) -> _PackageInfo:
    return _PackageInfo(
        name="example",
        version="1.0",
        location="/loc",
        editable_project_location=None,
        requires=[],
        required_by=[],
        installer="pip",
        metadata_version=metadata_version,
        classifiers=[],
        summary="",
        homepage="",
        project_urls=[],
        author="",
        author_email="",
        license="MIT",
        license_expression="MIT OR Apache-2.0",
        entry_points=[],
        files=None,
    )


@pytest.mark.parametrize(
    "metadata_version, expected, unexpected",
    [
        ("", "License: MIT", "License-Expression: MIT OR Apache-2.0"),
        ("2.4", "License-Expression: MIT OR Apache-2.0", "License: MIT"),
    ],
)
def test_print_results_license_for_metadata_version(
    caplog: pytest.LogCaptureFixture,
    metadata_version: str,
    expected: str,
    unexpected: str,
) -> None:
    caplog.set_level(logging.INFO)

    assert print_results(
        [_package_info(metadata_version)], list_files=False, verbose=False
    )

    messages = [record.getMessage() for record in caplog.records]
    assert expected in messages
    assert unexpected not in messages


def test_print_results_folds_multiline_fields(
    caplog: pytest.LogCaptureFixture,
) -> None:
    caplog.set_level(logging.INFO)
    info = _package_info("2.1")._replace(
        license="Copyright (c) Example\r\n\r\nAll rights reserved.",
        author="First Author\nSecond Author",
    )

    assert print_results([info], list_files=False, verbose=False)

    output = "\n".join(record.getMessage() for record in caplog.records) + "\n"
    headers = email.parser.Parser().parsestr(output, headersonly=True)
    assert headers["License"] == (
        "Copyright (c) Example\n        \n        All rights reserved."
    )
    assert headers["Author"] == "First Author\n        Second Author"
    # Fields after the multi-line ones are still parsed.
    assert headers["Location"] == "/loc"
    assert headers["Required-by"] == ""
