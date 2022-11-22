#!/usr/bin/env python3
#-*- coding: utf-8 -*-
from zipfile import ZipFile
from xml.etree import ElementTree
from io import BytesIO

from ghalton import GeneralizedHalton
from pyhull.delaunay import DelaunayTri

import math

# Name ggb vertices
def vertex_name(i): return 'roadmap_{{{:03}}}'.format(i)

# Name ggb edges
def edge_name(i, j): return 'roadmap_{{{:03}, {:03}}}'.format(i, j)

# Parse the initial ggb file
ggb = ZipFile('roadmap.ggb', mode='r')
xml = ggb.open('geogebra.xml')
tree = ElementTree.parse(xml)
xml.close()
ggb.close()

# Find the construction element in which to add sub elements
construction = tree.getroot().find('./construction')

# Generate graph vertices
#sequence = GeneralizedHalton(2)
#vertices = list()
#for i, (x, y) in enumerate(sequence.get(50)):
#	x *= 2000
#	y *= 3000
#	vertices.append((x, y))
side = 300
vertices = list()
imax = round(2000 / (side * math.sqrt(3) / 2))
jmax = round(3000 / side)
side = 2000 / imax / (math.sqrt(3) / 2)
for i in range(imax):
	for j in range(-1, jmax+1):
		x = side * (i * math.sqrt(3) / 2 + 0.5)
		y = side * (j + 0.5 * (i % 2)) + 1500 % side
		if y > 0 and y < 3000:
			vertices.append((x, y))

# Generate graph edges
delaunay= DelaunayTri(vertices,joggle=True)
edges = set()
for i, j, k in delaunay.vertices:
	edges.add((min(i, j), max(i, j)))
	edges.add((min(j, k), max(j, k)))
	edges.add((min(k, i), max(k, i)))

# Add vertices to the ggb file
for i, vertex in enumerate(vertices):
	element = ElementTree.SubElement(construction, 'element', type='point', label=vertex_name(i))
	ElementTree.SubElement(element, 'coords', x=str(vertex[0]), y=str(vertex[1]), z='1')
	ElementTree.SubElement(element, 'show', object='true', label='false')
	ElementTree.SubElement(element, 'condition', showObject='ShowRoadmap')

# Add edges to the ggb file
for i, j in edges:
	command = ElementTree.SubElement(construction, 'command', name='Segment')
	ElementTree.SubElement(command, 'input', a0=vertex_name(i), a1=vertex_name(j))
	ElementTree.SubElement(command, 'output', a0=edge_name(i, j))
	element = ElementTree.SubElement(construction, 'element', type='segment', label=edge_name(i, j))
	ElementTree.SubElement(element, 'show', object='true', label='false')
	ElementTree.SubElement(element, 'condition', showObject='ShowRoadmap')

# Save the new ggb file
stream = BytesIO()
tree.write(stream, encoding='utf-8', xml_declaration=True)
ggb = ZipFile('roadmap.ggb', mode='a')
ggb.writestr('geogebra.xml', stream.getvalue().decode('utf8'))
ggb.close()
