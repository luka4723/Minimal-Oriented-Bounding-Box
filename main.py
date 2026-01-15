import math
import pygame
import box
import convex
import sweep
from sweep import check_new
import tkinter as tk
from tkinter import filedialog
import ast



pygame.init()

t1,t2,t3,t4 = None,None,None,None

WIDTH, HEIGHT = 800, 600
PADDING = 10
red = (150, 0, 0)
green = (0, 150, 0)
col_connect = red
col_next = red
col_undo = red
col_clear = red
col_save = red
col_load = green
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Smallest bounding box of simple polygon")
font = pygame.font.Font(None, 25)

running = True
finished = False
clock = pygame.time.Clock()

points = []
segments = []
seg_it = 0
w_accum=0
bottom = pygame.Rect(0, HEIGHT-60, WIDTH, 60)
text = "Save"
w,_ = font.size(text)
save_text = font.render(text, True, (255, 255, 255))
save_button = pygame.Rect(PADDING+w_accum, bottom.y+PADDING, w+PADDING*2, 40)
text = "Load"
w_accum += w+PADDING*3
w,_ = font.size(text)
load_text = font.render(text, True, (255, 255, 255))
load_button = pygame.Rect(PADDING+w_accum, bottom.y+PADDING, w+PADDING*2, 40)
text = "End drawing"
w_accum += w+PADDING*3
w,_ = font.size(text)
connect_text = font.render(text, True, (255, 255, 255))
connect_button = pygame.Rect(PADDING+w_accum, bottom.y+PADDING, w+PADDING*2, 40)
text = "Next"
w_accum += w+PADDING*3
w,_ = font.size(text)
next_text = font.render(text, True, (255, 255, 255))
next_button = pygame.Rect(PADDING+w_accum, bottom.y+PADDING, w+PADDING*2, 40)
text = "Undo"
w_accum += w+PADDING*3
w,_ = font.size(text)
undo_text = font.render(text, True, (255, 255, 255))
undo_button = pygame.Rect(PADDING+w_accum, bottom.y+PADDING, w+PADDING*2, 40)
text = "Clear"
w_accum += w+PADDING*3
w,_ = font.size(text)
clear_text = font.render(text, True, (255, 255, 255))
clear_button = pygame.Rect(PADDING+w_accum, bottom.y+PADDING, w+PADDING*2, 40)
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
                        col_load = red
                        points.append((x, y))
                    else:
                        seg = sweep.segment((points[-1]), (x,y))
                        if check_new(new=seg,olds=segments):
                            points.append((x, y))
                            segments.append(seg)
                elif connect_button.collidepoint(x, y) and len(points) > 2:
                    seg = sweep.segment((points[-1]), points[0])
                    if check_new(new=seg, olds=segments):
                        finished = True
                        points.append(points[0])
                        segments.append(seg)
                        col_connect, col_next = red, green
                        col_save = green
                elif undo_button.collidepoint(x, y) and len(points) > 0:
                    points.pop()
                    if len(points) > 1:
                        segments.pop()
                    if len(points) ==0:
                        col_load = green
                elif clear_button.collidepoint(x, y):
                    segments.clear()
                    points.clear()
                    col_connect,col_next,col_undo,col_clear = red, red, red ,red
                    col_load = green
                elif load_button.collidepoint(x,y):
                    if col_load == green:
                        root = tk.Tk()
                        root.withdraw()

                        file_path = filedialog.askopenfilename(
                            title="Load",
                            defaultextension=".txt",
                            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
                        )

                        if file_path:
                            with open(file_path, "r", encoding="utf-8") as f:
                                points = ast.literal_eval(f.readline().strip())
                                segments_data = ast.literal_eval(f.readline().strip())
                                segments = [sweep.segment((x1, x2), (y1, y2)) for x1, x2, y1, y2 in segments_data]

                                finished = True
                                col_connect, col_next = red, green
                                col_save = green
                                col_load = red
            elif next_button.collidepoint(x, y):
                if len(hull_points)>0:
                    if not min_found:
                        #hull_points, hull_segments = sweep.make_ccw(hull_points,hull_segments)  #trebalo bi da radi i bez
                        #bounding_box = box.box(hull_segments[seg_it], hull_points)
                        bounding_box = box.box2(hull_segments[seg_it], hull_points)
                        width  = math.sqrt((bounding_box[1][0]-bounding_box[0][0])**2+(bounding_box[1][1]-bounding_box[0][1])**2)
                        height = math.sqrt((bounding_box[2][0]-bounding_box[1][0])**2+(bounding_box[2][1]-bounding_box[1][1])**2)
                        curr_surface = round(width * height)

                        text = "Cur surf: " + str(curr_surface)
                        cur_w, _ = font.size(text)
                        cur_text = font.render(text, True, (255, 255, 255))

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

                        text = "Cur surf: " + str(min_surf)
                        cur_w, _ = font.size(text)
                        cur_text = font.render(text, True, (255, 255, 255))

                        min_found2 = True
                        col_next = red
                else:
                    hull_points = convex.findConvexHull(points)
                    for i in range(0, len(hull_points) - 1):
                        hull_segments.append((hull_points[i],hull_points[i+1]))
                    hull_segments.append((hull_points[-1],hull_points[0]))
            elif save_button.collidepoint(x, y):
                root = tk.Tk()
                root.withdraw()

                file_path = filedialog.asksaveasfilename(
                    title="Save",
                    defaultextension=".txt",
                    filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
                )

                if file_path:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(points.__str__())
                        f.write("\n")
                        f.write(segments.__str__())

    if len(points) > 0 and finished == False:
        col_undo = green
        col_clear = green
    else:
        col_undo = red
        col_clear = red

    screen.fill((10, 10, 10))

    if len(points) > 2:
        closing_line = sweep.segment(points[0], points[-1])
        if check_new(new=closing_line, olds=segments) and not finished:
            col_connect = green
            pygame.draw.lines(screen, (255, 0, 0), False,(closing_line.p1,closing_line.p2), 2)
        else:
            col_connect = red
    else:
        col_connect = red

    if len(bounding_box) > 0:
        pygame.draw.polygon(screen, (0, 150, 0), bounding_box)

    if len(hull_points) >0 and not min_found2:

        for p in hull_points:
            pygame.draw.circle(screen, (0, 0, 255), p, 4)
        # if t1 is not None:
        #     pygame.draw.circle(screen, (255, 0, 0), t1, 4)
        #     pygame.draw.circle(screen, (255, 255, 0), t2, 4)
        #     pygame.draw.circle(screen, (0, 255, 255), t3, 4)
        #     pygame.draw.circle(screen, (255, 0, 255), t4, 4)

        pygame.draw.lines(screen, (0, 0, 255), False, hull_points, 2)
        pygame.draw.lines(screen, (0, 0, 255), False, (hull_points[0],hull_points[-1]), 2)


    else:
        for p in points:
            pygame.draw.circle(screen, (255, 255, 255), p, 4)

        if len(points) > 1:
            pygame.draw.lines(screen, (255, 255, 255), False, points, 2)

    pygame.draw.rect(screen, (100, 100, 100), bottom)
    pygame.draw.rect(screen, col_connect, connect_button)
    pygame.draw.rect(screen, col_next, next_button)
    pygame.draw.rect(screen, col_undo, undo_button)
    pygame.draw.rect(screen, col_clear, clear_button)
    pygame.draw.rect(screen, col_save, save_button)
    pygame.draw.rect(screen, col_load, load_button)
    screen.blit(connect_text, (connect_button.x + PADDING, connect_button.y + PADDING))
    screen.blit(next_text, (next_button.x + PADDING, next_button.y + PADDING))
    screen.blit(undo_text, (undo_button.x + PADDING, undo_button.y + PADDING))
    screen.blit(clear_text, (clear_button.x + PADDING, clear_button.y + PADDING))
    screen.blit(save_text, (save_button.x + PADDING, save_button.y + PADDING))
    screen.blit(load_text, (load_button.x + PADDING, load_button.y + PADDING))
    screen.blit(res_text, (WIDTH - PADDING - res_w, bottom[1] + 2 * PADDING))
    screen.blit(cur_text, (WIDTH - PADDING - cur_w - res_w - PADDING, bottom[1] + 2 * PADDING))


    pygame.display.flip()
    clock.tick(60)

pygame.quit()
