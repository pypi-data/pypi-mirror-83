# StrawberryPy
### Graphical animation module.

## How To Use
### Basic elements
* Every animation needs an engine. You can declare a engine variable like this: `eng = strawberrypy.Engine((resX, resY), fps)`
* Next, append layers to the engine: `eng.AddLayer(layer)` The layers will be rendered in order, with the first layer on the bottom.
* Layers can be declared like this: `layer = strawberrypy.shapes.Layer()`
* Layers contain shapes, added like this: `layer.Add(strawberrypy.shapes.(some shape))`

### Avaliable shapes
* Polygon: strawberrypy.Polygon(((vert1X, vert1Y), (vert2X, vert2Y)), (R, G, B))