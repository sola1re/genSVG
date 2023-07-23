#Inspired by Quantum algorithm from Qiskit Camp Africa 2019
#https://github.com/nixkj/qprocgen


import numpy as np
from numpy import pi, sqrt, round

while True:
    seed = input('Provide an even number of integers: ')
    if len(seed) % 2 == 0 and seed.isdigit():
        break
    print("Invalid input. The seed should be of even length and contain only numbers 0-9.")

print("Seed is:", seed)

xmlDecl = '<?xml version="1.0" standalone="no"?>'
svgOpen = '<svg width="15cm" height="15cm" viewBox="0 0 1000 1000" xmlns="http://www.w3.org/2000/svg" version="1.1"> '
svgTitle = '  <title>Seed: '+seed+'</title> '
svgPathStart = '<path d="'
svgClose = '</svg>'

padding_left = 50
padding_top = 50

def svgPath(pathCoords, r=10, g=150, b=44):
    pathDef = ''.join(pathCoords)
    pathString = '<path d="'+pathDef+'" fill="rgb('+str(r)+', '+str(b)+', '+str(b)+')"  /> '
    return pathString


def get_variation(pos, seed=10):
    (x, y) = pos

    #Random perturbation to x and y
    new_x = x + np.random.normal(0, 0.8, 1)
    new_y = y + np.random.normal(0, 0.8, 1)

    return new_x[0], new_y[0]

pathDefArray = []

#Original provided path used as seed
isFirst = True
for idx in range(len(seed)):
    if idx % 2 == 0:
        x = int(seed[idx])
        y = int(seed[idx+1])

        if isFirst:
            pathDefArray.append(' M ')
            isFirst = False
        else:
            pathDefArray.append(' L ')

        pathDefArray.append(str(100*x))
        pathDefArray.append(' ')

        pathDefArray.append(str(100*y))
        pathDefArray.append(' ')

def generateSeededPath(seededPathArr):
    _isFirst = True
    PathDefArray = []

    for idx in range(len(seededPathArr)):
        if idx % 2 == 0:
            x = int(seededPathArr[idx])
            y = int(seededPathArr[idx + 1])

            if _isFirst:
                PathDefArray.append(' M ')
                _isFirst = False
            else:
                PathDefArray.append(' L ')

            # Vary adjacent path
            new_x, new_y = get_variation((x, y), seed=8)

            PathDefArray.append(str(100*x))
            PathDefArray.append(' ')

            PathDefArray.append(str(100*y))
            PathDefArray.append(' ')

            # Add the updated coordinates to the path
            PathDefArray.append(str(100*new_x))
            PathDefArray.append(' ')

            PathDefArray.append(str(100*new_y))
            PathDefArray.append(' ')

    return PathDefArray

padding_left = 50
padding_top = 50


with open("SeededSVG.svg", "w+") as f:
    f.write(xmlDecl)

    viewBox_width = 1000 + 2 * padding_left
    viewBox_height = 1000 + 2 * padding_top
    f.write(f'<svg width="{viewBox_width}px" height="{viewBox_height}px" viewBox="{-padding_left} {-padding_top} {viewBox_width} {viewBox_height}" xmlns="http://www.w3.org/2000/svg" version="1.1"> ')

    f.write(svgTitle)

    f.write('<g>')

    for i in range(30):
        colour = list(np.random.choice(range(250), size=3))
        colourR = list(np.random.choice(range(10), size=3))

        f.write(svgPath(generateSeededPath(seed), colourR[0], colour[1], colour[2]))

    f.write('</g>')
    f.write(svgClose)