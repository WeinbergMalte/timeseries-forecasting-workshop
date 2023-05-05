import pytest

from timeseries.utils import ensure_iterable


@pytest.mark.parametrize(
    "input_, expected",
    [
        (0, [0]),
        ("0", ["0"]),
        ("Hello World", ["Hello World"]),
        ((1, 2), (1, 2)),
        (("A", "B"), ("A", "B")),
        ({1, 2, None}, {1, 2, None}),
        (range(3), range(3)),
        (None, [None]),
    ],
)
def test_ensure_iterable(input_, expected):
    result = ensure_iterable(input_)
    assert result == expected
