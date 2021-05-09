from fabric import FabrikSolver2D
import matplotlib.pyplot as plt
import math


def Angle(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    dX = x2 - x1
    dY = y2 - y1
    rads = math.atan2(-dY, dX) 
    return math.degrees(rads)


def Len(line):
    return ((line[0][0] - line[1][0])**2 + (line[0][1] - line[1][1])**2)**(0.5)


def AngleFromLines(lines):
   
    for line1 in lines:
        for line2 in lines:
            if line1 == line2:
                continue
            line1StPnt, line1EndPnt = line1
            line2StPnt, line2EndPnt = line2
            angle1 = Angle(line1StPnt, line1EndPnt)
            angle2 = Angle(line2StPnt, line2EndPnt)
            angle = abs(angle1 - angle2)
            return angle

def plotIterations(history):
    for i in range(len(history)):
        x = [0]
        y = [0]
        for segment in history[i]:
            x.append(segment.point[0])
            y.append(segment.point[1])

        plt.plot(x, y, label=("line " + str(i + 1)))
    plt.xlabel('x - axis')
    plt.ylabel('y - axis') 
    plt.title('Iterations history')
    plt.legend()
    plt.show()
lines = []
totalLinks = int(input("Total links: "))
for i in range(totalLinks):
    text = input("Enter coord[" + str(i) + "]: ")
    coord = tuple(float(x) for x in text.split())
    lastCoord = (0, 0)
    if (len(lines) > 0):
        lastCoord = lines[-1][1]
    lines.append(((lastCoord, coord)))
arm = FabrikSolver2D()
for i in range(len(lines)):
    linkLen = Len(lines[i])
    lastLine = ((-1, 0), (0, 0))
    if i != 0:
        lastLine = lines[i - 1]
    angle = AngleFromLines([lastLine, lines[i]])
    arm.addSegment(linkLen, angle)

final_coord = tuple(float(x) for x in input(
    "Enter end effector final position: ").split())

arm.compute(final_coord[0], final_coord[1])

print("total iterations: ", len(arm.history) - 1)

for segments in arm.history:
    text = ''
    for segment in segments:
        text += "[" + str(segment.point[0]) + ", " + \
            str(segment.point[1]) + "], "
    print(text[0:-2])
plotIterations(arm.history)
