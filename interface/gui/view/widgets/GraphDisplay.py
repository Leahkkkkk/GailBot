from typing import Dict, List, Tuple
from collections import deque
import math
from view.config.Style import Color, StyleSheet
from view.style.WidgetStyleSheet import SCROLL_BAR
from PyQt6.QtGui import QPainter, QFont
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsItem, QGraphicsLineItem, QGraphicsTextItem
from PyQt6.QtGui import QPen, QBrush,  QFont, QColor
from PyQt6.QtCore import QRectF, QLineF, Qt

NODE_COLOR = "#D3D3D3"
LINE_COLOR = "#000"
TEXT_COLOR = "#000"
class GraphDisplay(QGraphicsView):
    def __init__(self, dependencyGraph: Dict[str, List[str]]):
        super().__init__()
        print(dependencyGraph)
        self.graph = dependencyGraph
        self.nodes: Dict[str, Tuple ] = dict()
        self.width = 600
        self.height = 300
        self.scene = QGraphicsScene()
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.SmartViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setMinimumSize(QSize(self.width,self.height)) 
        self.verticalScrollBar().setStyleSheet(SCROLL_BAR)
        self.setStyleSheet(StyleSheet.basic)
        self.setScene(self.scene)
        self.draw_graph()
        
    def draw_graph(self):
        # add title
                # Create a QGraphicsTextItem and set its font and text
        title = QGraphicsTextItem("Plugin Map")
        titlefont = QFont("Arial", 22)
        titlefont.setWeight(600)
        title.setFont(titlefont)
    

        # Get the bounding rectangle of the scene and the title item
        scene_rect = self.scene.sceneRect()
        title_rect = title.boundingRect()

        # Set the position of the title item to the center of the scene's top edge
        title.setPos(200, 120)

        # Add the title item to the scene
        self.scene.addItem(title)
        poses = evenlyDistributedPoints(
            len(self.graph.keys()), 
            self.width , self.height )
        poses = sorted(poses, key =lambda p: (p[0], p[1]))
        sortedNodes = self.sort_nodes()
        sortedNodes.reverse()
        print(poses)
        print(sortedNodes)
        
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
                brush = QBrush()
                brush.setStyle(Qt.BrushStyle.SolidPattern)
                pen.setWidth(2)
                line = QGraphicsLineItem(node_item.x, node_item.y, neighbor_item.x, neighbor_item.y)
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
        brush.setColor(QColor(NODE_COLOR))
        painter.setBrush(brush)
        painter.drawEllipse(self.x - 45, self.y - 25, 90, 45)
        rect = QRectF(self.x - 35, self.y - 15, 90, 35)
        # painter.drawRect(rect)
       
        brush.setColor(QColor(TEXT_COLOR))
        painter.setBrush(brush)
        text = getShortHand(self.name)
        font = QFont("Arial", 12)
        font.setWeight(QFont.Weight.DemiBold)
        painter.setFont(font)
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

def evenlyDistributedPoints(n, x, y):
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

def getShortHand(name):
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