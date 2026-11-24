world = [[], [], []]  # 0: 배경, 1: 오브젝트, 2: UI

def add_object(o, depth=1):
    world[depth].append(o)

def add_objects(ol, depth=1):
    world[depth] += ol

def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            remove_collision_object(o)
            return

def update():
    for layer in world:
        for o in layer[:]:
            o.update()

def render():
    for layer in world:
        for o in layer[:]:
            o.draw()

def clear():
    for layer in world:
        layer.clear()
    collision_pairs.clear()

def collide(a,b):
    l_a, b_a, r_a, t_a = a.get_bb()
    l_b, b_b, r_b, t_b = b.get_bb()

    if r_a < l_b or l_a > r_b:
        return False
    if t_a < b_b or b_a > t_b:
        return False
    return True

collision_pairs = {}

def add_collision_pair(group, a, b):
    if group not in collision_pairs:
        collision_pairs[group] = [[], []]
    if a is not None and a not in collision_pairs[group][0]:
        collision_pairs[group][0].append(a)
    if b is not None and b not in collision_pairs[group][1]:
        collision_pairs[group][1].append(b)

# 충돌 페어로 등록된 오브젝트들에 대해 충돌을 검사하고 충돌 시 콜백 함수를 호출
def handle_collision():
    for group, pairs in collision_pairs.items():
        for a in pairs[0][:]:
            for b in pairs[1][:]:
                if a not in pairs[0] or b not in pairs[1]:
                    continue
                if collide(a, b):
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)
                    

def remove_collision_object(o) :
    for pairs in collision_pairs.values() :
        if o in pairs[0] :
            pairs[0].remove(o)
        if o in pairs[1] :
            pairs[1].remove(o)