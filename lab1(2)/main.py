a, b, c = map(int, input("Введите a, b, c: ").split(maxsplit=3))
d = b**2-4*a*c
if d==0:
    print(-b/(2*a))
elif d>0:
    x1 = (-b + d ** 0.5) / (2 * a)
    x2 = (-b - d ** 0.5) / (2 * a)
    print(x1,x2)
else:
    print("нет корней")

