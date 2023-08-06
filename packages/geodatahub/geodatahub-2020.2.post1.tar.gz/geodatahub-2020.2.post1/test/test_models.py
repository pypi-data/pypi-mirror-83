import pytest

from geodatahub.models import Dataset

@pytest.mark.models
def test_geom_to_wkt():
    # Test for polygons
    d = Dataset(
        datatype = "myType",
        result = {},
        distribution_info = {},
        projected_geometry = {"coordinates": [[[3.304003, 61.106058], [3.304003, 61.241526], [3.666384, 61.241526], [3.666384, 61.106058], [3.304003, 61.106058]]], "type": "Polygon"}
    )

    assert d.geom_to_wkt() == "POLYGON ((3.304003 61.106058, 3.304003 61.241526, 3.666384 61.241526, 3.666384 61.106058, 3.304003 61.106058))"

    # Test for points
    d = Dataset(
        datatype = "myType",
        result = {},
        distribution_info = {},
        projected_geometry = {
            "type": "Point",
            "coordinates": [
                5.64697265625,
                61.56457388515458
            ]
        }
    )

    assert d.geom_to_wkt() == "POINT (5.64697265625 61.56457388515458)"

    # Test for points
    d = Dataset(
        datatype = "myType",
        result = {},
        distribution_info = {},
        projected_geometry = {
            "type": "LineString",
            "coordinates": [ [30, 10], [10, 30], [40, 40]]
        }
    )

    assert d.geom_to_wkt() == "LINESTRING (30 10, 10 30, 40 40)"
