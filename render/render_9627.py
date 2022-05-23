'''
***************************************************
* author: Anestis Kaimakamidis 9627
* date: 31/3/22
* Triangle Shading
***************************************************
'''

import numpy as np


'''
function interpolate_color
inputs: * x1: int coordinate
        * x2: int coordinate
        * x: int coordinate
        * C1: point x1 rgb color (array 1x3)
        * C2: point x2 rgb color (array 1x3)

output: * C3: point x rgb color (array 1x3)
'''
def interpolate_color(x1, x2, x, C1, C2):
    C3 = np.zeros(3)
    if x1 != x2: 
        C3 = C1 + (x - x1) * (C2 - C1) / (x2 - x1) 
        return C3
    else:
        return C1

'''
function shade_tringle
inputs: * img: MxNx3 matrix representing the canvas (with existing triangles)
        * verts2d: 3x2 array of the triangle's vertexes coordinates
        * vcolors: 3x3 array of the triangle's vertexes colours
        * shade_t: shading technique (in this demo gouraud)

output: * img: the input img with one added shaded triangle
'''

def shade_triangle(img,verts2d,vcolors,shade_t, M, N):
    #functions of the three triangle lines (given y output x is produced)
    def line1(y, x):
        if verts2d[1,1] != verts2d[0,1]:
                return (y - verts2d[0,1]) / (verts2d[1,1] - verts2d[0,1]) * (verts2d[1,0]-verts2d[0,0]) + verts2d[0,0]
        else:
            return x

    def line2(y, x):
        if verts2d[2,1] != verts2d[1,1]:
            return (y - verts2d[1,1]) / (verts2d[2,1] - verts2d[1,1]) * (verts2d[2,0]-verts2d[1,0]) + verts2d[1,0]
        else:
            return x

    def line3(y, x):
        if verts2d[0,1] != verts2d[2,1]:
            return (y - verts2d[2,1]) / (verts2d[0,1] - verts2d[2,1]) * (verts2d[0,0]-verts2d[2,0]) + verts2d[2,0]
        else:
            return x

    lines = [line1, line2, line3]


    if shade_t == "gouraud":

        ykmin = np.zeros(len(verts2d))
        ykmax = np.zeros(len(verts2d))

        #find ykmin ykmax
        for i in range(len(verts2d)):
            ykmin[i] = min(verts2d[i, 1], verts2d[(i+1)%len(verts2d), 1])
            ykmax[i] = max(verts2d[i, 1], verts2d[(i+1)%len(verts2d), 1])

        #find ymin ymax
        ymin = int(min(ykmin))
        ymax = int(max(ykmax))
        peaks = np.zeros((2,5))
        lines_used = []
        
        #initialise peaks and lines_used
        lasti = []
        for i in range(len(verts2d)):
            if verts2d[i, 1] == ymin:
                peaks[0, :2] = verts2d[i]
                peaks[0, 2:] = vcolors[i]
                lines_used = [(i+len(verts2d)-1)%len(verts2d), i]
                lasti.append(i)
        if peaks[1][0] == 0:
            peaks[1] = peaks[0]
        if len(lasti) > 1:
            for j in range(2):
                lines_used[j] = (lasti[j] + 1) % 3


        #shade for each scanline y
        for y in range(ymin, ymax+1):
            #sort peaks
            peaks = peaks[peaks[: , 0].argsort()]
            cross_count = 0

            #for every x in the current scanline
            for x in range(M):
                #check if x is an intersection point
                for k in range(2):
                    if x == peaks[k,0]:
                        cross_count += 1

                #if cross_count is odd paint pixel
                if cross_count % 2 == 1:
                    #colour interpolation according to x position
                    img[x, y] = interpolate_color(peaks[0, 0], peaks[1, 0], x, peaks[0, 2:], peaks[1, 2:])
            

            #update lines_used
            for j in range(3):
                if y + 1 == ykmin[j]:
                    if min(ykmax) != max(ykmax):
                        lines_used.append(j)
                if y == ykmax[j] and y != ymax:
                    if min(ykmin) != max(ykmin):
                        lines_used.remove(j)
            peaks = np.zeros((2,5))

            #update peaks and peak colours
            for j in range(2):
                peaks[j, 0] = int(lines[lines_used[j]](y+1, x))
                peaks[j, 1] = y+1
                peaks_of_line = [lines_used[j] , (lines_used[j]+1)%len(verts2d)]
                peaks[j, 2:] = interpolate_color(verts2d[peaks_of_line[0], 1], verts2d[peaks_of_line[1], 1], peaks[j, 1], vcolors[peaks_of_line[0]], vcolors[peaks_of_line[1]])
    elif shade_t == "flat":
        #colour all pixels of a triangle with the mean of its vertexes
        color = np.mean(vcolors, axis=0)

        #find ykmin ykmax
        ykmin = np.zeros(len(verts2d))
        ykmax = np.zeros(len(verts2d))
        for i in range(len(verts2d)):
            ykmin[i] = min(verts2d[i, 1], verts2d[(i+1)%len(verts2d), 1])
            ykmax[i] = max(verts2d[i, 1], verts2d[(i+1)%len(verts2d), 1])

        #find ymin ymax
        ymin = int(min(ykmin))
        ymax = int(max(ykmax))
        peaks = np.zeros((2,2))
        lines_used = []
        

        #initialise peaks and lines_used
        lasti = []
        for i in range(len(verts2d)):
            if verts2d[i, 1] == ymin:
                peaks[0] = verts2d[i]
                lines_used = [(i+len(verts2d)-1)%len(verts2d), i]
                lasti.append(i)
        if peaks[1][0] == 0:
            peaks[1] = peaks[0]
        if len(lasti) > 1:
            for j in range(2):
                lines_used[j] = (lasti[j] + 1) % 3


        #shade for each scanline y
        for y in range(ymin, ymax+1):
            #sort peaks
            peaks = peaks[peaks[: , 0].argsort()]
            cross_count = 0

            #for every x in the current scanline
            for x in range(N):
                #check if x is an intersection point
                for k in range(2):
                    if x == peaks[k,0]:
                        cross_count += 1

                #if cross_count is odd paint pixel
                if cross_count % 2 == 1:
                    img[x, y] = color
            
            #update lines_used
            for j in range(3):
                if y + 1 == ykmin[j]:
                    if min(ykmax) != max(ykmax):
                        lines_used.append(j)
                if y == ykmax[j] and y != ymax:
                    if min(ykmin) != max(ykmin):
                        lines_used.remove(j)
           
            #update peaks and peak colours
            peaks = np.zeros((2,2))
            for j in range(2):
                peaks[j, 0] = int(lines[lines_used[j]](y+1, x))
                peaks[j, 1] = y+1
    else:
        print("Not a valid shading technique")
                

    return img


'''
function render
inputs: * verts2d: Lx2 array (coordinates of the vertexes of the triangles)
        * faces: Kx3 array (pointers to verts2d pointing each triangle's vertexes)
        * vcolors: Lx3 array (colours of the vertexes of the triangles)
        * depth: Lx1 array (depth of every vertex)
        * shade_t: shading technique

output: * image: MxNx3 matrix image generated
'''
def render(verts2d, faces, vcolors, depth, shade_t, M=512, N=512):
    image=np.full((M,N,3),255,np.uint8)


    #triangle depth: depth of each triangle along with its faces
    triangle_depth = np.zeros((len(faces), 4))
    depths = np.zeros(3)

    #find triangle depth
    for i in range(len(faces)):
        for j in range(3):
            depths[j] = depth[faces[i, j]]
        triangle_depth[i, 0] = np.mean(depths)
        triangle_depth[i, 1:] = faces[i]

    #sort triangle_depth from max to min depth (first column)
    triangle_depth = triangle_depth[triangle_depth[:, 0].argsort()]
    triangle_depth = np.flip(triangle_depth, axis=0)


    #for every triangle call shade_triangle
    for i in range(len(triangle_depth)):
        verts = np.zeros((3,2))
        colors = np.zeros((3,3))
        for j in range(3):
            verts[j] = verts2d[int(triangle_depth[i,j+1])]
            colors[j] = vcolors[int(triangle_depth[i,j+1])]
        
        if(shade_t == "gouraud"): image = shade_triangle(image, verts, colors*255, shade_t, M, N)
        elif(shade_t == "flat"): image = shade_triangle(image, verts, np.flip(colors)*255, shade_t, M, N)

    return image

