import random
import statistics

# todo:
# put in a series simulator

r = lambda: random.choice([1,2,3,4,5,6])

quiet = False


def single(attacking=3, defending=2, silent=False):
    if attacking <= 1 or defending <= 0:
        print("Please attack with more than 1 unit or defend with more than 0 units.")
        return
    s = True if attacking == 2 or defending == 1 else False

    a = [r(), r(), r()] if attacking > 3 else [r(), r(), 0] if attacking > 2 else [r(), 0, 0]
    d = [r(), r()] if defending > 1 else [r(), 0]
    if not silent:
        print("ATK: ", a, ", DEF: :", d)
    a.sort()
    d.sort()
    a = a[::-1]
    d = d[::-1]

    acost = 0
    dcost = 0
    if (a[0] > d[0]):
        dcost = dcost + 1
    else:
        acost = acost + 1

    if not s:
        if (a[1] > d[1]):
            dcost = dcost + 1
        else:
            acost = acost + 1

    if not silent:
        print("ATK loses ", acost, ", DEF loses", dcost)
    return (acost, dcost)


# 0 is normal input, >0 is auto, -1 is stop, -2 is instant
def continuous_input():
    u_in = input()
    uisint = False
    try:
        int(u_in)
        uisint = True
    except:
        pass

    if u_in == "s" or u_in == "stop":
        return -1
    if u_in == "i" or u_in == "instant":
        return -2
    elif uisint:
        auto = int(u_in)
        if auto >= 1:
            return auto
    return 0


def continuous(a=100, d=100, cs=False, auto=0):
    if not cs:
        print("Press 'Enter' to roll once, input ('instant'|'i') for instant completion,")
        print("or enter a number of rolls to be completed")

    if auto == 0:
        u_in = continuous_input()
        if u_in == -1:
            return
        elif u_in == -2:
            auto = 100000000000000000000
        elif u_in > 0:
            auto = u_in-1

    while a > 1 and d > 0:
        # if quiet mode is on, silence auto continuous until final
        silent = cs
        if quiet and auto > 0:
            silent = True

        lost = single(a, d, silent)
        a = a - lost[0]
        d = d - lost[1]
        if not silent:
            print("attack: ", a, ", defense: ", d)

        if auto == 0 and a > 1 and d > 0:
            u_in = continuous_input()
            if u_in == -1:
                break
            elif u_in == -2:
                auto = 100000000000000000000
            elif u_in > 0:
                auto = u_in-1
        else:
            auto = auto - 1

    if not cs:
        print("The battle ended with ", a, " attackers, and ", d, " defenders.")

    return (a, d)


def sim():
    u_in = input("Input the attackers and defenders: ")
    u_in = u_in.split()
    num = input("Input the number of times you would like to run: ")
    out = []
    u_in = [int(i) for i in u_in]
    for i in range(int(num)):
        res = continuous(u_in[0], u_in[1], True, 100000000000000)
        out.append((res[0]-1)-res[1])

    output = open('out.csv', 'w')
    print(out, file=output)
    print("Mean: ", statistics.mean(out))
    print("Median: ", statistics.median(out))
    print("Stdev: ", statistics.pstdev(out))
    output.close()



while True:
    u_in = input("How many attackers and defenders? (separate with a space): ")
    u_in = u_in.split()
    u_in_int = []
    u_in_is_int = True
    for i in u_in:
        try:
            b = int(i)
            if b <= 0:
                u_in_is_int = False
            u_in_int.append(b)
        except:
            u_in_is_int = False

    if len(u_in) == 0:
        pass
    elif u_in[0] == "quiet" or u_in[0] == "q":
        print("quiet mode toggled!")
        quiet=True if not quiet else False
    elif u_in[0] == "help" or u_in[0] == "h":
        print("type 'q' or 'quiet' to silence unnecessary printing.")
        print("type 'e' or 'exit' to exit.")
    elif u_in[0] == "sim":
        print("entering simulator")
        sim()
    elif u_in[0] == "d" or u_in[0] == "die":
        print(r())
    elif u_in[0] == "exit" or u_in[0] == "e":
        break
    elif u_in_is_int and len(u_in_int) == 2:
        continuous(*u_in_int)
    else:
        print("Please input something valid")
