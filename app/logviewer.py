import sys
import os
import pygame
import time
import queue
import threading
from common import flatten, GameState, Point, ATTACKER_ID, DEFENDER_ID

# print(flatten((None, (1559918512028036058, ((112, (None, (4, (16, None)))), None)))))

pygame.init()
sz = 3

display_info = pygame.display.Info()
w = display_info.current_w
h = display_info.current_h
print("try to guess screen size:", w, h)
screen = pygame.display.set_mode([w, h])
print("Loading font...", end="")
sys.stdout.flush()
font = pygame.font.SysFont("verdanattf", 18)
small_font = pygame.font.SysFont("verdanattf", 10)
font_ship_info = pygame.font.SysFont("verdanattf", 16)
print("done")


def parse_line(line):
    line = line.replace("nil", "None")
    try:
        a = eval(line)
        f = flatten(a)
        # print(a, "--f->", f)
        return f
    except Exception as e:
        print("WARNING: Can't parse line - ", line, e)
        return [0]


def to_screen(pos):
    return (w // 2 + sz * pos.x, h // 2 + sz * pos.y)


def add_input(input_queue):
    while True:
        line = sys.stdin.readline()
        input_queue.put(line)


def draw_centered_rect(color, size, width):
    top_left = to_screen(Point(-size, -size))
    bottom_right = to_screen(Point(size, size))
    rect = (top_left[0], top_left[1], bottom_right[0] - top_left[0], bottom_right[1] - top_left[1])
    pygame.draw.rect(screen, color, rect, width=width)


def main():
    input_queue = queue.Queue()

    input_thread = threading.Thread(target=add_input, args=(input_queue,))
    input_thread.daemon = True
    input_thread.start()

    outs, ins = [], []

    turn = 0
    total_turns = 0
    prev_turn = -1

    pygame.key.set_repeat(500, 30)

    if len(sys.argv) > 1 and sys.argv[1] == '-s':
        d = os.path.dirname(os.path.realpath(__file__))
        fname = os.path.join(d, "logs", "commands_{:.0f}".format(time.time()))
        cf = open(fname, "w")
    else:
        cf = None

    global sz
    while True:
        while not input_queue.empty():
            line = input_queue.get()
            if line.startswith("->"):
                if cf is not None:
                    cf.write(line)
                outs.append(parse_line(line[3:].strip()))
            if line.startswith("<-"):
                if cf is not None:
                    cf.write(line)
                ins.append(parse_line(line[3:].strip()))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    sz += 1
                if event.key == pygame.K_2 and sz > 1:
                    sz -= 1
                if event.key == pygame.K_o:
                    if turn > 1:
                        turn -= 1
                if event.key == pygame.K_p:
                    if turn + 1 < total_turns:
                        turn += 1

        total_turns = min(len(ins), len(outs))
        if total_turns == 0:
            continue

        try:
            gs = GameState(ins[turn])
        except:
            if turn == 0 and total_turns > 1:
                turn += 1
                gs = GameState(ins[turn])

        screen.fill(0)
        if turn != prev_turn:
            print("=" * 20)
            print("turn {}/{}".format(turn, total_turns))
            print("sent -> {}".format(outs[turn]))
            print("got  <- {}".format(ins[turn]))
            prev_turn = turn

        last_text_pos_y = 40
        for sh in gs.ships:
            if sh.player_type == gs.my_type:
                color = (0, 192, 0)
            else:
                color = (192, 0, 0)

            screen_pos = to_screen(sh.pos)
            if sh.player_type == DEFENDER_ID:
                pygame.draw.circle(screen, color, screen_pos, 15, 2)
            else:
                pygame.draw.rect(screen, color, (screen_pos[0] - 15, screen_pos[1] - 15, 30, 30), 2)
            pygame.draw.line(screen, color, screen_pos, to_screen(sh.pos + sh.speed), 2)

            screen.blit(font.render(str(sh.ship_id), 1, color), (screen_pos[0] - 35, screen_pos[1] - 12))
            screen.blit(small_font.render("{}+{}".format(sh.pos, sh.speed).replace(" ", ""), 1, color), (screen_pos[0] + 20, screen_pos[1] - 6))

            text = '(id:{}, energy:{}, shoot_energy:{}, rest:{}, health:{}, tired:{}/{})'.format(
                sh.ship_id,
                sh.energy,
                sh.shoot_energy,
                sh.rest,
                sh.health,
                sh.tiredness,
                sh.tiredness_limit)

            for m in sh.prev_moves:
                text += "  " + str(m)
                if m.move_type == 2:
                    target_pos = to_screen(m.pos())
                    pygame.draw.line(screen, color, screen_pos, target_pos, 1 + m.args[2] // 10)

            text_info = font_ship_info.render(text, 1, color)
            screen.blit(text_info, (10, last_text_pos_y))
            last_text_pos_y += 24

        border_color = (200, 200, 200)
        draw_centered_rect(border_color, gs.world_size, 2)
        draw_centered_rect(border_color, gs.planet_size, 0)  # fill

        tt = font.render('turn {}/{}; sz = {}; finished = {}'.format(turn, total_turns, sz, gs.game_finished),
                         1, (192, 192, 192))
        # print(dir(tt.get_rect()))
        screen.blit(tt, (10, 5))

        pygame.display.update()


if __name__ == "__main__":
    main()
