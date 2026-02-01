import pygame
import math

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# --- Kubus 3D ---
cube_vertices = [
    [-1,-1,-1],
    [ 1,-1,-1],
    [ 1, 1,-1],
    [-1, 1,-1],
    [-1,-1, 1],
    [ 1,-1, 1],
    [ 1, 1, 1],
    [-1, 1, 1]
]

cube_edges = [(0,1),(1,2),(2,3),(3,0),
              (4,5),(5,6),(6,7),(7,4),
              (0,4),(1,5),(2,6),(3,7)]

cube_pos = [-2,0,6]   # posisi ke kiri
cube_rot = [0,0,0]
cube_scale = 100

# --- Persegi 2D ---
square = [
    [0.5,0.5],
    [0.5,-0.5],
    [-0.5,-0.5],
    [-0.5,0.5]
]

square_pos = [300,300]  # kanan layar

# --- Fungsi Proyeksi 3D ke 2D ---
def project_point(p):
    factor = 200/(p[2]+cube_pos[2])
    x = (p[0]+cube_pos[0])*factor + WIDTH//4
    y = (p[1]+cube_pos[1])*factor + HEIGHT//2
    return (int(x),int(y))

def rotate3D(points, ax, ay, az):
    rotated=[]
    for x,y,z in points:
        # rotasi X
        cosx,sinx=math.cos(ax),math.sin(ax)
        y,z = y*cosx - z*sinx, y*sinx + z*cosx
        # rotasi Y
        cosy,siny=math.cos(ay),math.sin(ay)
        x,z = x*cosy + z*siny, -x*siny + z*cosy
        # rotasi Z
        cosz,sinz=math.cos(az),math.sin(az)
        x,y = x*cosz - y*sinz, x*sinz + y*cosz
        rotated.append([x,y,z])
    return rotated

# --- Transformasi 2D ---
def rotate2D(points, angle):
    rad=math.radians(angle)
    cos,sin=math.cos(rad),math.sin(rad)
    return [[x*cos - y*sin, x*sin + y*cos] for x,y in points]

def scale2D(points, sx, sy):
    return [[x*sx,y*sy] for x,y in points]

def shear2D(points, shx, shy):
    return [[x+shx*y, y+shy*x] for x,y in points]

def reflect2D(points, axis='x'):
    if axis=='x':
        return [[x,-y] for x,y in points]
    else:
        return [[-x,y] for x,y in points]

# --- Main Loop ---
running=True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

    keys=pygame.key.get_pressed()

    # --- Kontrol Kubus ---
    if keys[pygame.K_w]: cube_pos[1]+=0.1
    if keys[pygame.K_s]: cube_pos[1]-=0.1
    if keys[pygame.K_a]: cube_pos[0]-=0.1
    if keys[pygame.K_d]: cube_pos[0]+=0.1
    if keys[pygame.K_r]: cube_pos[2]-=0.1
    if keys[pygame.K_f]: cube_pos[2]+=0.1

    if keys[pygame.K_i]: cube_rot[0]+=0.05
    if keys[pygame.K_k]: cube_rot[0]-=0.05
    if keys[pygame.K_j]: cube_rot[1]+=0.05
    if keys[pygame.K_l]: cube_rot[1]-=0.05
    if keys[pygame.K_u]: cube_rot[2]+=0.05
    if keys[pygame.K_o]: cube_rot[2]-=0.05

    if keys[pygame.K_z]: cube_scale*=0.95
    if keys[pygame.K_x]: cube_scale*=1.05

    # --- Kontrol Persegi ---
    if keys[pygame.K_UP]: square_pos[1]-=5
    if keys[pygame.K_DOWN]: square_pos[1]+=5
    if keys[pygame.K_LEFT]: square_pos[0]-=5
    if keys[pygame.K_RIGHT]: square_pos[0]+=5

    if keys[pygame.K_q]: square=rotate2D(square,5)
    if keys[pygame.K_e]: square=rotate2D(square,-5)

    if keys[pygame.K_t]: square=scale2D(square,1,1.1)
    if keys[pygame.K_g]: square=scale2D(square,1,0.9)
    if keys[pygame.K_y]: square=scale2D(square,1.1,1)
    if keys[pygame.K_h]: square=scale2D(square,0.9,1)

    if keys[pygame.K_1]: square=shear2D(square,0.1,0)
    if keys[pygame.K_2]: square=shear2D(square,-0.1,0)
    if keys[pygame.K_3]: square=shear2D(square,0,0.1)
    if keys[pygame.K_4]: square=shear2D(square,0,-0.1)

    if keys[pygame.K_5]: square=reflect2D(square,'x')
    if keys[pygame.K_6]: square=reflect2D(square,'y')

    # --- Render ---
    screen.fill((30,30,30))

    # Kubus (ungu)
    rotated = rotate3D(cube_vertices, *cube_rot)
    projected = [project_point(v) for v in rotated]
    for edge in cube_edges:
        pygame.draw.line(screen,(150,0,200),projected[edge[0]],projected[edge[1]],2)

    # Persegi (hijau)
    pts = [(square_pos[0]+x*100, square_pos[1]+y*100) for x,y in square]
    pygame.draw.polygon(screen,(0,255,0),pts,2)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()