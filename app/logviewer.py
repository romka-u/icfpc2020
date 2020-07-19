import sys
import pygame
import queue
import threading
from common import flatten, GameState, Point

# print(flatten((None, (1559918512028036058, ((112, (None, (4, (16, None)))), None)))))

pygame.init()
sz = 7

display_info = pygame.display.Info()
w = display_info.current_w
h = display_info.current_h
print('try to guess screen size:', w, h)


screen = pygame.display.set_mode([w, h])
font = pygame.font.SysFont("verdanattf", 18)


def parse_line(line):
    a = eval(line)
    f = flatten(a)
    # print(a, "--f->", f)
    return f

def to_screen(pos):
    return (w // 2 + sz * pos.x, h // 2 + sz * pos.y)

def add_input(input_queue):
    while True:
        line = sys.stdin.readline()
        input_queue.put(line)

def main():
    input_queue = queue.Queue()

    input_thread = threading.Thread(target=add_input, args=(input_queue,))
    input_thread.daemon = True
    input_thread.start()

    outs, ins = [], []

    turn = 1
    prev_turn = -1

    pygame.key.set_repeat(500, 30)

    global sz
    while True:
        while not input_queue.empty():
            line = input_queue.get()
            if line.startswith("->"):
                outs.append(parse_line(line[3:].strip()))
            if line.startswith("<-"):
                ins.append(parse_line(line[3:].strip()))

        total_turns = min(len(ins), len(outs))
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

        if total_turns == 0:
            continue

        gs = GameState(ins[turn])
        screen.fill(0)
        if turn != prev_turn:
            print("=" * 20)
            print("turn {}/{}".format(turn, total_turns))
            print("sent -> {}".format(outs[turn]))
            print("got  <- {}".format(ins[turn]))
            prev_turn = turn

        for sh in gs.ships:
            if sh.player_type == gs.my_type:
                color = (0, 192, 0)
            else:
                color = (192, 0, 0)

            pygame.draw.circle(screen, color, to_screen(sh.pos), 20, 3)
            pygame.draw.line(screen, color, to_screen(sh.pos), to_screen(sh.pos + sh.speed), 3)

        tt = font.render('turn {}/{}; sz = {}; finished = {}'.format(turn, total_turns, sz, gs.game_finished),
                         1, (192, 192, 192))
        # print(dir(tt.get_rect()))
        screen.blit(tt, (10, 5))
        pygame.display.update()


if __name__ == "__main__":
    main()
