from source.controller.assembly.Shape import Square, Rectangle, CircumscribedCircle

# c1 = Circle(10, 10, 5)
sq1 = Square(10, 10, 5)
sq2 = Rectangle(10, 10, 5, 6)
sq3 = Square(10, 10, 5)
# print(sq1)
# c2 = InscribedCircle(sq1)
c3 = CircumscribedCircle(sq2)
# print(c2)
# print(c3)
# print(sq1.intersects(sq2))
print(c3.x)

# print(sq2.same(sq1))
