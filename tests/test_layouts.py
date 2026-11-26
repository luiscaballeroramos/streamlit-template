import unittest
from unittest.mock import patch

from layouts import Layout, render_layout


class LayoutTests(unittest.TestCase):
    def test_rejects_non_rectangular_areas_and_invalid_weights(self):
        with self.assertRaisesRegex(ValueError, "rectangulo"):
            Layout((("main", "main"), ("main", "details")), (1, 1), (1, 1))
        for weight in (0, -1, float("inf"), float("nan")):
            with self.subTest(weight=weight), self.assertRaises(ValueError):
                Layout((("main",),), (weight,), (1,))

    def test_rejects_different_regions_before_rendering(self):
        horizontal = Layout((("main",),), (1,), (1,))
        vertical = Layout((("details",),), (1,), (1,))
        with patch("layouts.st") as streamlit:
            with self.assertRaisesRegex(ValueError, "mismas zonas"):
                render_layout(key="example", horizontal=horizontal, vertical=vertical, regions={})
            streamlit.container.assert_not_called()

    def test_renders_content_once_despite_two_distributions(self):
        horizontal = Layout((("main", "details"),), (70, 30), (1,))
        vertical = Layout((("details",), ("main",)), (1,), (25, 75))
        calls = []
        with patch("layouts.st"):
            render_layout(
                key="example", horizontal=horizontal, vertical=vertical,
                regions={"main": lambda: calls.append("main"), "details": lambda: calls.append("details")},
            )
        self.assertEqual(calls, ["main", "details"])
