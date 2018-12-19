# v1 = 1
# v5 = 5

# v4 = v1*v5

# if v4 == v2:
#     v0 += 1

# v5 += 1
# if v5 <= v2:
#     goto l_3
# else:
#     v1 += 1
#     if v1 <= v2:
#         goto l_2
#     else:
#         return

def start(v2):
    v0 = 0
    v1 = 1
    while v1 <= v2:
        v5 = 1
        while v5 <= v2:
            v4 = v1 * v5
            if v4 == v2:
                v0 += v1
            v5 += 1
        v1 += 1
    print(v0)


def opt(v2):
    v0 = 0
    for i in range(1,v2+1):
        if v2%i == 0:
            v0 += i
    print(v0)

v0 = 1

v2 = (2*2)*19*11
v4 = 8*22 + 12
v2 = v2 + v4
if v0:
    v4 = (27*28 + 29)*30*14*32
    v2 += v4
    v0 = 0
print(v2, v4)
opt(v2)

