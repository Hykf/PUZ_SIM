import pygame
import sys
import random
import math

pygame.init()
WIDTH, HEIGHT = 1000, 850 
UI_HEIGHT = 60            
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PUZ SIM")

BG_COLOR = (250, 250, 252)       
UI_BG_COLOR = (230, 230, 240)
NODE_COLOR = (200, 200, 210)     
NODE_BORDER = (60, 60, 70)    
EDGE_COLOR = (60, 60, 70)        
BTN_COLOR = (180, 180, 190)
BTN_HOVER = (150, 150, 170)
BTN_ACTIVE = (100, 200, 120)
BTN_STOP_RED = (220, 100, 100)
BTN_START_GREEN = (100, 200, 120)
TEXT_COLOR = (50, 50, 60)
SLIDER_BG = (160, 160, 170)
SLIDER_FILL = (80, 120, 180)

FONT = pygame.font.SysFont("arial", 14, bold=True)
FONT_SMALL = pygame.font.SysFont("arial", 12)

CURRENT_COUNT = 70      
GRAVITY_MULT = 1.0      
PARAMS = {}

nodes = []
system_temperature = 1.0
cycles_colored = False 

###############################

class Button:
    def __init__(self, x, y, w, h, text, callback, color=BTN_COLOR):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.callback = callback
        self.base_color = color
        self.hovered = False
        self.dynamic_color = color 
    
    def draw(self, surface):
        col = self.dynamic_color
        if self.hovered: 
            col = (min(255, col[0]+30), min(255, col[1]+30), min(255, col[2]+30))
        
        pygame.draw.rect(surface, col, self.rect, border_radius=5)
        pygame.draw.rect(surface, (100, 100, 100), self.rect, 1, border_radius=5)
        
        txt_surf = FONT.render(self.text, True, TEXT_COLOR)
        txt_rect = txt_surf.get_rect(center=self.rect.center)
        surface.blit(txt_surf, txt_rect)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and self.hovered:
            if self.callback: self.callback()

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (180, 180, 180)
        self.text = text
        self.txt_surface = FONT.render(text, True, TEXT_COLOR)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = (255, 255, 255) if self.active else (180, 180, 180)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                global CURRENT_COUNT
                if self.text.isdigit():
                    val = int(self.text)
                    if val < 2: val = 2
                    if val > 600: val = 600
                    CURRENT_COUNT = val
                    reset_sim()
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if event.unicode.isdigit(): 
                    self.text += event.unicode
            self.txt_surface = FONT.render(self.text, True, TEXT_COLOR)

    def draw(self, surface):
        bg = (255, 255, 255) if self.active else (220, 220, 220)
        pygame.draw.rect(surface, bg, self.rect, border_radius=4)
        pygame.draw.rect(surface, (100, 100, 100), self.rect, 1, border_radius=4)
        surface.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 8))

class Slider:
    def __init__(self, x, y, w, min_val, max_val, initial):
        self.rect = pygame.Rect(x, y, w, 20)
        self.min_val = min_val
        self.max_val = max_val
        self.val = initial
        self.dragging = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                self.update_val(event.pos[0])
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.update_val(event.pos[0])

    def update_val(self, mx):
        ratio = (mx - self.rect.x) / self.rect.w
        ratio = max(0, min(1, ratio))
        self.val = self.min_val + ratio * (self.max_val - self.min_val)
        global GRAVITY_MULT
        GRAVITY_MULT = self.val

    def draw(self, surface):
        label = FONT_SMALL.render(f"Center Gravity: {self.val:.2f}x", True, TEXT_COLOR)
        surface.blit(label, (self.rect.x, self.rect.y - 18))
        pygame.draw.rect(surface, SLIDER_BG, (self.rect.x, self.rect.centery - 2, self.rect.w, 4), border_radius=2)
        ratio = (self.val - self.min_val) / (self.max_val - self.min_val)
        pygame.draw.rect(surface, SLIDER_FILL, (self.rect.x, self.rect.centery - 2, self.rect.w * ratio, 4), border_radius=2)
        handle_x = self.rect.x + (self.rect.w * ratio)
        pygame.draw.circle(surface, (100, 100, 120), (int(handle_x), int(self.rect.centery)), 8)

class Node:
    def __init__(self, idx, x, y):
        self.id = idx
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(0, 0)
        self.target_id = None
        self.radius = PARAMS["RADIUS"]
        self.dragging = False
        self.popularity = 0 
        self.cycle_color = None 

    def apply_force(self, force):
        self.vel += force

    def update(self, temperature):
        if self.dragging: return

        if temperature > 0:
            if self.vel.length() > PARAMS["MAX_FORCE"]:
                self.vel.scale_to_length(PARAMS["MAX_FORCE"])

            self.pos += self.vel * temperature
            
            friction = 0.85
            if self.popularity >= 1: friction = 0.6
            if self.popularity >= 2: friction = 0.3
            self.vel *= friction

            m = self.radius + 2
            if self.pos.x < m: self.pos.x = m; self.vel.x *= -0.5
            if self.pos.x > WIDTH - m: self.pos.x = WIDTH - m; self.vel.x *= -0.5
            if self.pos.y < m + UI_HEIGHT: self.pos.y = m + UI_HEIGHT; self.vel.y *= -0.5
            if self.pos.y > HEIGHT - m: self.pos.y = HEIGHT - m; self.vel.y *= -0.5


##############################

def adapt_parameters(n):
    """Adjusts physics parameters based on the number of nodes"""
    global PARAMS
    PARAMS = {
        "RADIUS": 12,              
        "REPULSION": 600.0,         
        "SPRING_LEN": 50.0,         
        "SPRING_STR": 0.15,         
        "CENTER_GRAVITY": 0.15,     
        "MAX_FORCE": 4.0,
        "MIN_TEMP": 0.005,
        "ARROW_SIZE": 10,
        "COOLING_RATE": 0.99
    }
    
    if n <= 25:
        PARAMS.update({"RADIUS": 13, "REPULSION": 600.0, "SPRING_LEN": 60.0, 
                       "CENTER_GRAVITY": 0.12, "COOLING_RATE": 0.985, "ARROW_SIZE": 11})
    elif n <= 60:
        PARAMS.update({"RADIUS": 10, "REPULSION": 450.0, "SPRING_LEN": 45.0, 
                       "CENTER_GRAVITY": 0.10, "COOLING_RATE": 0.992, "ARROW_SIZE": 8})
    else:
        PARAMS.update({"RADIUS": 7, "REPULSION": 280.0, "SPRING_LEN": 30.0, 
                       "CENTER_GRAVITY": 0.25, "COOLING_RATE": 0.998, "ARROW_SIZE": 6})



def calculate_physics(nodes):
    center = pygame.Vector2(WIDTH/2, (HEIGHT + UI_HEIGHT)/2)
    
    for i, node in enumerate(nodes):
        if node.dragging: continue
        force = pygame.Vector2(0, 0)

        for j, other in enumerate(nodes):
            if i != j:
                diff = node.pos - other.pos
                dist_sq = diff.length_squared()
                if dist_sq == 0:
                    diff = pygame.Vector2(random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5))
                    dist_sq = diff.length_squared()
                
                min_dist = (PARAMS["RADIUS"] * 2.5) ** 2
                if dist_sq < min_dist: dist_sq = min_dist
                force += diff.normalize() * (PARAMS["REPULSION"] / math.sqrt(dist_sq))

        if node.target_id is not None:
            target = nodes[node.target_id]
            diff = target.pos - node.pos
            force += diff.normalize() * (diff.length() - PARAMS["SPRING_LEN"]) * PARAMS["SPRING_STR"]

        to_center = center - node.pos
        dist = to_center.length()
        g_val = PARAMS["CENTER_GRAVITY"] * GRAVITY_MULT
        force += to_center.normalize() * (dist * (g_val + dist * 0.0001))

        node.apply_force(force)

def color_cycles(nodes):
    visited_global = set()
    for node in nodes:
        if node.id in visited_global: continue
        path = []
        curr = node
        path_ids = set()
        
        while curr.id not in visited_global:
            visited_global.add(curr.id)
            path.append(curr)
            path_ids.add(curr.id)
            if curr.target_id is not None: curr = nodes[curr.target_id]
            else: break 
            
            if curr.id in path_ids:
                cycle_nodes = []
                in_cycle = False
                for p in path:
                    if p.id == curr.id: in_cycle = True
                    if in_cycle: cycle_nodes.append(p)
                
                if len(cycle_nodes) >= 2:#min nodes to make cycle
                    rand_color = (random.randint(50, 220), random.randint(50, 220), random.randint(50, 220))
                    for c_node in cycle_nodes: c_node.cycle_color = rand_color
                break

def draw_arrow(surface, start, end, target_node, color, thickness=1):
    direction = end - start
    length = direction.length()
    target_r = target_node.radius

    if length > PARAMS["RADIUS"] + target_r:
        direction = direction.normalize()
        start_adj = start + direction * PARAMS["RADIUS"]
        end_adj = end - direction * (target_r + (PARAMS["ARROW_SIZE"] * 0.6))
        
        pygame.draw.line(surface, color, start_adj, end_adj, thickness)

        angle = math.atan2(direction.y, direction.x)
        sz = PARAMS["ARROW_SIZE"]
        if thickness > 2: sz += 2
            
        p1 = end_adj
        p2 = end_adj - pygame.Vector2(math.cos(angle + 0.5), math.sin(angle + 0.5)) * sz
        p3 = end_adj - pygame.Vector2(math.cos(angle - 0.5), math.sin(angle - 0.5)) * sz
        pygame.draw.polygon(surface, color, [p1, p2, p3])


def reset_sim():
    global nodes, system_temperature, cycles_colored
    adapt_parameters(CURRENT_COUNT)
    nodes = []
    system_temperature = 1.0
    cycles_colored = False
    
    cx, cy = WIDTH//2, (HEIGHT+UI_HEIGHT)//2
    start_spread = 20 if CURRENT_COUNT <= 50 else 150
    
    for i in range(CURRENT_COUNT):
        x = cx + random.randint(-start_spread, start_spread)
        y = cy + random.randint(-start_spread, start_spread)
        nodes.append(Node(i, x, y))
    
    counts = {i: 0 for i in range(CURRENT_COUNT)}
    for node in nodes:
        possible = [n.id for n in nodes if n.id != node.id]
        target = random.choice(possible)
        node.target_id = target
        counts[target] += 1
    
    for node in nodes:
        node.popularity = counts[node.id]
        bonus = 3 if CURRENT_COUNT < 50 else 2
        if node.popularity > 1: node.radius += bonus

def toggle_sim():
    global system_temperature, cycles_colored
    if system_temperature > 0:
        system_temperature = 0
    else:
        system_temperature = 0.5 
        cycles_colored = False 

def apply_input_count():
    global CURRENT_COUNT
    if input_box.text.isdigit():
        val = int(input_box.text)
        if val < 2: val = 2
        if val > 600: val = 600
        CURRENT_COUNT = val
        reset_sim()

###############################################

if __name__ == "__main__":

    input_box = InputBox(60, 15, 60, 30, text=str(CURRENT_COUNT))
    btn_reset = Button(130, 15, 70, 30, "RESET", apply_input_count)
    btn_toggle = Button(220, 15, 100, 30, "STOP", toggle_sim, color=BTN_STOP_RED)
    slider_grav = Slider(WIDTH - 180, 25, 150, 0.0, 3.0, 1.0)

    buttons = [btn_reset, btn_toggle] 

    reset_sim()
    clock = pygame.time.Clock()
    running = True
    dragged_node = None

    while running:
        mx, my = pygame.mouse.get_pos()
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT: running = False
            
            input_box.handle_event(e)
            slider_grav.handle_event(e)
            for b in buttons: b.handle_event(e)

            if e.type == pygame.MOUSEBUTTONDOWN and my > UI_HEIGHT:
                for n in nodes:
                    if n.pos.distance_to((mx, my)) < n.radius + 10:
                        n.dragging = True
                        dragged_node = n
                        if system_temperature > 0:
                            system_temperature = 0.5 
                            cycles_colored = False 
                        break
            
            if e.type == pygame.MOUSEBUTTONUP:
                if dragged_node:
                    dragged_node.dragging = False
                    dragged_node = None
            
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                reset_sim()

        if dragged_node:
            dragged_node.pos = pygame.Vector2(mx, my)
            if dragged_node.pos.y < UI_HEIGHT + 10: dragged_node.pos.y = UI_HEIGHT + 10
            dragged_node.vel = pygame.Vector2(0,0)

        if system_temperature > 0:
            btn_toggle.text = "STOP"
            btn_toggle.dynamic_color = BTN_STOP_RED
        else:
            btn_toggle.text = "RESUME"
            btn_toggle.dynamic_color = BTN_START_GREEN

        if system_temperature > PARAMS["MIN_TEMP"]:
            system_temperature *= PARAMS["COOLING_RATE"]
            calculate_physics(nodes)
            for n in nodes: n.update(system_temperature)
        else:
            system_temperature = 0
            if not cycles_colored:
                color_cycles(nodes)
                cycles_colored = True

        screen.fill(BG_COLOR)
        
        for n in nodes:
            if n.target_id is not None:
                target = nodes[n.target_id]
                
                line_col = EDGE_COLOR
                line_thick = 2 if CURRENT_COUNT < 60 else 1
                
                if n.cycle_color:
                    line_col = n.cycle_color
                    line_thick += 2 
                    
                draw_arrow(screen, n.pos, target.pos, target, line_col, line_thick)
        
        for n in nodes:
            fill_col = NODE_COLOR
            if n.cycle_color: fill_col = n.cycle_color
            if n.dragging: fill_col = (150, 200, 255)
            
            border_col = NODE_BORDER
            pygame.draw.circle(screen, border_col, (int(n.pos.x), int(n.pos.y)), n.radius + 1)
            pygame.draw.circle(screen, fill_col, (int(n.pos.x), int(n.pos.y)), n.radius - 1)

        pygame.draw.rect(screen, UI_BG_COLOR, (0, 0, WIDTH, UI_HEIGHT))
        pygame.draw.line(screen, (200, 200, 210), (0, UI_HEIGHT), (WIDTH, UI_HEIGHT), 1)
        
        screen.blit(FONT.render("Nodes:", True, TEXT_COLOR), (15, 22))
        input_box.draw(screen)
        for b in buttons: b.draw(screen)
        slider_grav.draw(screen)

        if system_temperature > 0:
            pygame.draw.line(screen, (100, 200, 100), (0, UI_HEIGHT-2), (WIDTH * (1.0 - system_temperature), UI_HEIGHT-2), 3)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()