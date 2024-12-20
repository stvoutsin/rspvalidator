import shutil
import sys
from collections.abc import Callable
from io import BytesIO
from pathlib import Path
from typing import Any

import pytest
from PIL import Image
from pixelmatch.contrib.PIL import pixelmatch

__all__ = ["SnapshotComparatorService"]


class SnapshotComparatorService:
    """Utility class for comparing visual snapshots in tests."""

    @staticmethod
    def create_snapshot_fixture(pytestconfig: Any,
                                request: Any,
                                browser_name: str) -> Callable:
        """Create a fixture for snapshot comparison.

        Parameters
        ----------
        pytestconfig : Any
            The pytest configuration object
        request : Any
            The pytest request object
        browser_name : str
            Name of the browser being used

        Returns
        -------
        Callable
            A function to compare snapshots
        """
        test_function_name = request.node.name.split('[')[0]
        test_name = f"{test_function_name}[{sys.platform!s}]"

        def compare(
                img: bytes,
                *,
                threshold: float = 0.1,
                name: str = f'{test_name}.png',
                fail_fast: bool = False
        ) -> None:
            """Compare the given image against a stored snapshot.

            Parameters
            ----------
            img : bytes
                The image data to compare
            threshold : float, optional
                Comparison threshold value, by default 0.1
            name : str, optional
                Name of the snapshot file
            fail_fast : bool, optional
                Whether to fail on first pixel difference

            Raises
            ------
            pytest.fail
                If images don't match or new snapshot is created
            """
            test_file_name = str(Path(request.node.fspath).name).strip('.py')

            filepath = (
                    Path(request.node.fspath).parent.resolve()
                    / 'snapshots'
                    / test_file_name
                    / test_function_name
            )
            filepath.mkdir(parents=True, exist_ok=True)
            file = filepath / name

            # Create a dir where all snapshot test failures will go
            results_dir_name = (Path(request.node.fspath).parent.resolve()
                                / "snapshot_tests_failures")
            test_results_dir = (results_dir_name
                                / test_file_name
                                / test_function_name
                                / test_name)

            # Remove a single test's past run dir with actual, diff and expected images
            if test_results_dir.exists():
                shutil.rmtree(test_results_dir)
            if not file.exists():
                file.write_bytes(img)
                pytest.fail("New snapshot(s) created. Please review images")

            # Compare images
            img_a = Image.open(BytesIO(img))
            img_b = Image.open(file)
            img_diff = Image.new("RGBA", img_a.size)

            mismatch = pixelmatch(
                img_a,
                img_b,
                img_diff,
                threshold=threshold,
                fail_fast=fail_fast
            )

            if mismatch > 0:
                test_results_dir.mkdir(parents=True, exist_ok=True)
                img_diff.save(f'{test_results_dir}/Diff_{name}')
                img_a.save(f'{test_results_dir}/Actual_{name}')
                img_b.save(f'{test_results_dir}/Expected_{name}')
                pytest.fail("Snapshots DO NOT match!")

        return compare
