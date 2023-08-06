# StrawberryPy
### Graphical animation module.

## How To Use
### Basic elements
* Every animation needs an scene. You can declare a scene variable like this: `scene = strawberrypy.Scene2D((resX, resY), fps)`
* Next, append layers to the engine: `scene.AddLayer(layer)` The layers will be rendered in order, with the first layer on the bottom.
* Layers can be declared like this: `layer = strawberrypy.Layer()`
* Layers contain shapes, added like this: `layer.Add(strawberrypy.shapes.(some shape))`

### Avaliable shapes
* Polygon: `strawberrypy.shapes.Polygon(((vert1X, vert1Y), (vert2X, vert2Y)), (R, G, B), borderWidth)`
* Circle: `strawberrypy.shapes.Circle((centerX, centerY), radius, (R, G, B), borderWidth)`
