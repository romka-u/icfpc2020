import sys
import pygame
from common import flatten

# print(flatten((None, (1559918512028036058, ((112, (None, (4, (16, None)))), None)))))

pygame.init()
w = 1600
h = 1000
sz = 10
screen = pygame.display.set_mode([w, h])
font = pygame.font.SysFont("verdanattf", 18)


def parse_line(line):
    a = eval(line)
    f = flatten(a)
    # print(a, "--f->", f)
    return f

def main():
    outs, ins = [], []
    for line in sys.stdin:
        try:
            if line.startswith("->"):
                outs.append(parse_line(line[3:].strip()))
            if line.startswith("<-"):
                ins.append(parse_line(line[3:].strip()))
        except:
            break

    if len(outs) > len(ins):
        outs = outs[:len(ins)]

    turn = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    sz += 1
                if event.key == pygame.K_2 and sz > 1:
                    sz -= 1
                if event.key == pygame.K_o:
                    if turn > 0:
                        turn -= 1
                if event.key == pygame.K_p:
                    if turn + 1 < len(outs):
                        turn += 1

        screen.fill(0)
        print("=" * 20)
        print("turn {}/{}".format(turn, len(outs)))
        print("sent -> {}".format(outs[turn]))
        print("got  <- {}".format(ins[turn]))
        tt = font.render('turn {}/{}'.format(turn, len(outs)), 1, (192, 192, 192))
        # print(dir(tt.get_rect()))

        screen.blit(tt, (10, 5))
        pygame.display.update()


if __name__ == "__main__":
    main()
