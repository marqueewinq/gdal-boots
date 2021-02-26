from osgeo import gdal, ogr


class GeometryBuilder:

    @classmethod
    def create(cls, geometry):
        if isinstance(geometry, str):
            return ogr.CreateGeometryFromJson(geometry)

        handler = getattr(cls, 'create_{}'.format(geometry['type'].lower()))
        return handler(geometry['coordinates'])

    @classmethod
    def create_polygon(cls, coordinates):
        polygon = ogr.Geometry(ogr.wkbPolygon)
        for ring_coords in coordinates:
            ring = ogr.Geometry(ogr.wkbLinearRing)
            for point in ring_coords:
                ring.AddPoint(*point)
            polygon.AddGeometry(ring)
        return polygon

    @classmethod
    def create_line_string(cls, coordinates):
        line = ogr.Geometry(ogr.wkbLineString)
        for point in coordinates:
            line.AddPoint(*point)
        return line

    @classmethod
    def create_multipolygon(cls, coordinates):
        multipolygon = ogr.Geometry(ogr.wkbMultiPolygon)

        for polygon_coordinates in coordinates:
            polygon = cls.create_polygon(polygon_coordinates)
            multipolygon.AddGeometry(polygon)

        return multipolygon
