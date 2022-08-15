from noise import pnoise2

array = []
scale = 100
size = 10000
for i in range(size):
    for j in range(size):
        p = pnoise2(
            (i/scale)+0,
            (j/scale)+0,
            octaves=4,
            persistence=0.6,
            lacunarity=2,
            repeatx=size,
            repeaty=size,
            base=1
        )
        array.append(p)

print("minimum:", min(array))
print("maximum:", max(array))