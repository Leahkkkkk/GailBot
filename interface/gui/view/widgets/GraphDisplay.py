'''
File: GraphDisplay.py
Project: GailBot GUI
File Created: 2023/04/01
Author: Siara Small  & Vivian Li
-----
Last Modified:2023/05/19
Modified By:  Siara Small  & Vivian Li
-----
Description: implementation of a graph display widget that display a graph 
             stored in an adjacency list 
'''

from typing import Dict, List, Tuple
from collections import deque
import math
from view.config.Style import  STYLE_DATA
from PyQt6.QtGui import QPainter, QFont
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import  (
    QGraphicsView, 
    QGraphicsScene, 
    QGraphicsItem,
    QGraphicsLineItem, 
    QGraphicsTextItem)
from PyQt6.QtGui import QPen, QBrush,  QFont, QColor
from PyQt6.QtCore import QRectF, QLineF, Qt


class GraphDisplay(QGraphicsView):
    def __init__(self, dependencyGraph: Dict[str, List[str]]):
        """ display a dependencyGraph

        Args:
            dependencyGraph (Dict[str, List[str]]): the adjacency list representation 
                                                    of a dependency graph, 
                                                    the key is current node, 
                                                    and the value is the list 
                                                    of nodes current node depends on 
        """
        super().__init__()
        self.graph = dependencyGraph
        self.nodes: Dict[str, Tuple ] = dict()
        self.width = 600
        self.height = 300
        self.scene = QGraphicsScene()
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform |
                           QPainter.RenderHint.Antialiasing)

        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.SmartViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setMinimumSize(QSize(self.width,self.height)) 
        self.verticalScrollBar().setStyleSheet(STYLE_DATA.StyleSheet.SCROLL_BAR)
        self.setStyleSheet(STYLE_DATA.StyleSheet.basic)
        self.setScene(self.scene)
        self.draw_graph()
        
    def draw_graph(self):
        # add title
        # Create a QGraphicsTextItem and set its font and text
        title = QGraphicsTextItem("Plugin Map")
        title.setDefaultTextColor(QColor(STYLE_DATA.Color.MAIN_TEXT))
        titlefont = QFont("Arial", 22)
        titlefont.setWeight(600)
        title.setFont(titlefont)

        # Set the position of the title item to the center of the scene's top edge
        title.setPos(200, 120)
        
        # Add the title item to the scene
        poses = evenlyDistributedPoints(
            len(self.graph.keys()), 
            self.width , self.height )
        poses = sorted(poses, key =lambda p: (p[0], p[1]))
        sortedNodes = self.sort_nodes()
        sortedNodes.reverse()
  
        for node, pos in zip (sortedNodes, poses):
            newNode = NodeItem(node, pos[0], pos[1])
            self.scene.addItem(newNode)
            self.nodes[node] = newNode
            
        for node, neighbors in self.graph.items():
            node_item = self.nodes[node]
            for neighbor in neighbors:
                neighbor_item = self.nodes.get(neighbor, None)
                if neighbor_item is None:
                    self.nodes[neighbor] = neighbor_item
                pen = QPen(Qt.PenStyle.SolidLine)
                pen.setWidth(2)
                pen.setColor(QColor(STYLE_DATA.Color.MAIN_TEXT))
                line = QGraphicsLineItem(node_item.x, 
                                         node_item.y, 
                                         neighbor_item.x, 
                                         neighbor_item.y)
                line.setPen(pen)
                line.setZValue(-1) 
                self.scene.addItem(line)
       
    def sort_nodes(self) -> List[str]:
        return topologicalSort(self.graph)
    
class NodeItem(QGraphicsItem):
    def __init__(self, name, x, y):
        super().__init__()
        self.name = name
        self.x = x
        self.y = y
        
    def boundingRect(self):
        return QRectF(self.x, self.y, 30, 10)
    
    def paint(self, painter, option, widget):
        brush = QBrush()
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        brush.setColor(QColor(STYLE_DATA.Color.HIGHLIGHT))
        painter.setBrush(brush)
        painter.drawEllipse(self.x - 45, self.y - 25, 90, 45)
        rect = QRectF(self.x - 35, self.y - 15, 90, 35)
        # painter.drawRect(rect)
        pen = QPen()
        pen.setColor(QColor(STYLE_DATA.Color.MAIN_TEXT)) 
        brush.setColor(QColor(STYLE_DATA.Color.MAIN_TEXT))
        painter.setBrush(brush)
        text = getShortHand(self.name)
        font = QFont("Arial", 12)
        font.setWeight(QFont.Weight.DemiBold)
        painter.setFont(font)
        painter.setPen(pen)
        painter.drawText(rect,text)

class EdgeItem(QGraphicsLineItem):
    def __init__(self, x1, y1, x2, y2):
        super().__init__()
        self.x1 = x1 
        self.y1 = y1 
        self.x2 = x2 
        self.y2 = y2 
        
    def paint(self, painter, option, widget):
        painter.drawLine(QLineF(self.x1, self.y1, self.x2, self.y2))

# Utility function 

def topologicalSort(graph):
    # Initialize a dictionary to store the number of incoming edges for each node
    in_degrees = {node: 0 for node in graph}

    # Calculate the number of incoming edges for each node
    for node in graph:
        for dependent in graph[node]:
            in_degrees[dependent] += 1

    # Initialize a queue with nodes that have no incoming edges
    queue = deque([node for node in graph if in_degrees[node] == 0])

    # Initialize an empty list to store the sorted nodes
    sorted_nodes = []

    # Process the queue
    while queue:
        # Remove a node from the queue
        node = queue.popleft()

        # Add the node to the sorted list
        sorted_nodes.append(node)

        # Remove the node's outgoing edges
        for dependent in graph[node]:
            in_degrees[dependent] -= 1
            if in_degrees[dependent] == 0:
                queue.append(dependent)

    # Check if there is a cycle in the graph
    if len(sorted_nodes) != len(graph):
        raise ValueError("Graph contains a cycle")

    return sorted_nodes

def evenlyDistributedPoints(n, x, y) -> List[Tuple[int, int]]:
    """ given the width x and heighy y of the space, return a list of positions 
        of n points that will be evenly distributed in the space
    """
    positions = []
    num_rows = int(math.sqrt(n))
    num_cols = math.ceil(n / num_rows)
    x_step = x / (num_cols)
    y_step = y / (num_rows) - 5
    for i in range(num_rows):
        for j in range(num_cols):
            if len(positions) == n:
                break
            pos_x = int ((j + 1) * x_step - x // 2)
            pos_y = int ((i + 1) * y_step - y // 2)
            positions.append((pos_x, pos_y))
    return positions

def getShortHand(name) -> str:
    """ given a plugin name, shrink the name of the plugin if the name is too
        long to be able to fit the word into the graph
    """
    if "Plugin" in name:
        res = name.replace("Plugin", "")
    else: 
        res = name
    if len(res) > 10:
        new_text="" 
        count = 0
        for i in range(len(res)):
            if res[i].isupper():
                count += 1
                if count == 2:
                    new_text += '\n'
            new_text += res[i]
        return new_text
    return res