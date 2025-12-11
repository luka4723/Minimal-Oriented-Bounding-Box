import math

import pygame

import box
import convex
import sweep
from sweep import check_new

pygame.init()

WIDTH, HEIGHT = 800, 600
PADDING = 10
red = (150, 0, 0)
green = (0, 150, 0)
col1 = red
col2 = red
col3 = red
col4 = red
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Smallest bounding box of simple polygon")
font = pygame.font.Font(None, 25)

running = True
finished = False
clock = pygame.time.Clock()

points = []
segments = sweep.SortedList()
seg_it = 0

bottom = pygame.Rect(0, HEIGHT-60, WIDTH, 60)
text = "End drawing"
w,_ = font.size(text)
connect_text = font.render(text, True, (255, 255, 255))
connect_button = pygame.Rect((WIDTH-PADDING)/2-w-PADDING*2, bottom.y+PADDING, w+PADDING*2, 40)
text = "Next"
w,_ = font.size(text)
next_text = font.render(text, True, (255, 255, 255))
next_button = pygame.Rect((WIDTH+PADDING)/2, bottom.y+PADDING, w+PADDING*2, 40)
text = "Undo"
w,_ = font.size(text)
undo_text = font.render(text, True, (255, 255, 255))
undo_button = pygame.Rect((WIDTH-PADDING)/2-connect_button.w-w-PADDING*2-PADDING, bottom.y+PADDING, w+PADDING*2, 40)
text = "Clear"
w,_ = font.size(text)
clear_text = font.render(text, True, (255, 255, 255))
clear_button = pygame.Rect((WIDTH-PADDING)/2-connect_button.w-w-PADDING*2-PADDING-undo_button.w-PADDING, bottom.y+PADDING, w+PADDING*2, 40)
text = "Min surf: -"
res_w,_ = font.size(text)
res_text = font.render(text, True, (255, 255, 255))
text = "Cur surf: -"
cur_w,_ = font.size(text)
cur_text = font.render(text, True, (255, 255, 255))


hull_points = []
hull_segments = []
bounding_box = []

min_surf = 9999999
min_index = 0
min_box = []
min_found = False
min_found2 = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if not finished:
                if not bottom.collidepoint(x, y):
                    if len(points) == 0:
                        points.append((x, y))
                    else:
                        seg = sweep.segment((points[-1]), (x,y))
                        if check_new(new=seg,olds=segments):
                            points.append((x, y))
                            segments.add(seg)
                elif connect_button.collidepoint(x, y) and len(points) > 2:
                    seg = sweep.segment((points[-1]), points[0])
                    if check_new(new=seg, olds=segments):
                        finished = True
                        points.append(points[0])
                        segments.add(seg)
                        col1, col2 = red, green
                elif undo_button.collidepoint(x, y) and len(points) > 0:
                    points.pop()
                    if len(points) > 1:
                        segments.pop()
                elif clear_button.collidepoint(x, y):
                    segments.clear()
                    points.clear()
                    col1,col2,col3,col4 = red, red, red ,red
            elif next_button.collidepoint(x, y):
                if len(hull_points)>0:
                    if not min_found:
                        bounding_box = box.test(hull_segments[seg_it],hull_points)
                        width  = math.sqrt((bounding_box[1][0]-bounding_box[0][0])**2+(bounding_box[1][1]-bounding_box[0][1])**2)
                        height = math.sqrt((bounding_box[2][0]-bounding_box[1][0])**2+(bounding_box[2][1]-bounding_box[1][1])**2)
                        curr_surface = round(width * height)

                        text = "Cur surf: " + str(curr_surface)
                        cur_w, _ = font.size(text)
                        cur_text = font.render(text, True, (255, 255, 255))

                        print(curr_surface,min_surf)
                        if curr_surface < min_surf:
                            min_box = bounding_box
                            min_index = seg_it
                            min_surf = curr_surface

                            text = "Min surf: " + str(min_surf)
                            res_w, _ = font.size(text)
                            res_text = font.render(text, True, (255, 255, 255))

                        seg_it = seg_it+1
                        if seg_it == len(hull_segments):
                            min_found = True
                    else:
                        bounding_box = min_box
                        min_found2 = True
                        col2 = red
                else:
                    hull_points = convex.findConvexHull(points)
                    for i in range(0, len(hull_points) - 1):
                        hull_segments.append((hull_points[i],hull_points[i+1]))
                    hull_segments.append((hull_points[-1],hull_points[0]))


    if len(points) > 0 and finished == False:
        col3 = green
        col4 = green
    else:
        col3 = red
        col4 = red

    screen.fill((10, 10, 10))
    pygame.draw.rect(screen, (100,100,100), bottom)
    pygame.draw.rect(screen, col1, connect_button)
    pygame.draw.rect(screen, col2, next_button)
    pygame.draw.rect(screen, col3, undo_button)
    pygame.draw.rect(screen, col4, clear_button)
    screen.blit(connect_text, (connect_button.x+PADDING, connect_button.y+PADDING))
    screen.blit(next_text, (next_button.x+PADDING, next_button.y+PADDING))
    screen.blit(undo_text, (undo_button.x+PADDING, undo_button.y+PADDING))
    screen.blit(clear_text, (clear_button.x+PADDING, clear_button.y+PADDING))
    screen.blit(res_text,(WIDTH-PADDING-res_w,bottom[1]+2*PADDING))
    screen.blit(cur_text,(WIDTH-PADDING-cur_w-res_w-PADDING,bottom[1]+2*PADDING))

    if len(points) > 2:
        closing_line = sweep.segment(points[0], points[-1])
        if check_new(new=closing_line, olds=segments) and not finished:
            col1 = green
            pygame.draw.lines(screen, (255, 0, 0), False,(closing_line.p1,closing_line.p2), 2)
        else:
            col1 = red
    else:
        col1 = red

    if len(bounding_box) > 0:
        pygame.draw.polygon(screen, (0, 150, 0), bounding_box)

    if len(hull_points) >0 and not min_found2:

        for p in hull_points:
            pygame.draw.circle(screen, (0, 0, 255), p, 4)

        pygame.draw.lines(screen, (0, 0, 255), False, hull_points, 2)
        pygame.draw.lines(screen, (0, 0, 255), False, (hull_points[0],hull_points[-1]), 2)

    else:
        for p in points:
            pygame.draw.circle(screen, (255, 255, 255), p, 4)

        if len(points) > 1:
            pygame.draw.lines(screen, (255, 255, 255), False, points, 2)



    pygame.display.flip()
    clock.tick(60)

pygame.quit()
