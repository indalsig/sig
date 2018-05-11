from sqlalchemy import Column, Integer, String, BigInteger, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from indalsig.db import Base
from geoalchemy2 import Geometry


class Way(Base):

    __tablename__ = 'sig_ways'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    city = Column(String(2))
    openstreetmap_id = Column(BigInteger)
    way_nodes = relationship("WayNode", cascade="delete, delete-orphan")
    geom = Column(Geometry('LINESTRING'))

    def __init__(self):
        self.id = None
        self.name = None
        self.city = None
        self.openstreetmap_id = None
        self.way_nodes = []

    def search_way_node_by_id(self, osm_id):
        for way_node in self.way_nodes:
            if way_node.node.openstreetmap_id == osm_id:
                return way_node.node

    def search_way_node_by_id_and_seq(self, osm_id, seq):
        for way_node in self.way_nodes:
            if way_node.node.openstreetmap_id == osm_id and way_node.seq == seq:
                return way_node

    def delete_invalid_relationships(self, nodes):
        for way_node in self.way_nodes:
            if way_node.node.openstreetmap_id not in nodes:
                self.way_nodes.remove(way_node)


class Node(Base):

    __tablename__ = 'sig_nodes'

    id = Column(Integer, primary_key=True)
    lat = Column(Numeric)
    lng = Column(Numeric)
    openstreetmap_id = Column(BigInteger)
    postcode = Column(Integer)


class WayNode(Base):

    __tablename__ = 'sig_ways_nodes'

    way_id = Column(Integer, ForeignKey('sig_ways.id', ondelete='CASCADE'), primary_key=True)
    node_id = Column(Integer, ForeignKey('sig_nodes.id', ondelete='CASCADE'), primary_key=True)
    seq = Column(Integer, primary_key=True)

    way = relationship('Way', backref="waynodes")
    node = relationship('Node')

    def __init__(self):
        self.seq

class Address(Base):

    __tablename__ = 'sig_addresses'

    id = Column(Integer, primary_key=True)
    formatted_address = Column(String(255))
    postcode = Column(Integer)
    street_name = Column(String(255))
    street_number = Column(String(50))
    lon = Column(Numeric(13, 10))
    lat = Column(Numeric(13, 10))

class Postcode(Base):

    __tablename__ = 'sig_postcodes'

    id = Column(Integer, primary_key=True)
    postcode = Column(Integer)
    geom = Column(Geometry('MULTIPOLYGON'))