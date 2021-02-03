# 生成a-z键
# for i in range(97, 123):
#     print('key_' + chr(i) + ' =', '0x%X' % (0xC0000 + i - 97))

# 生成所有数字
# for i in range(0, 10):
#     print('key_' + str(i) + ' =', '0x%X' % (0xC0019 + i + 1))

# 生成所有功能键
# for i in range(1, 13):
#     print('key_F' + str(i) + ' =', '0x%X' % (0xC0023 + i + 1))

# 生成A-Z键
# for i in range(65, 91):
#     print('key_' + chr(i) + ' =', '0x%X' % ((0xC0000 + i - 65) + 0xC0033))

# 生成特殊符号
# for i in range(33, 48):
#     """对应的是'!' ~ '?' """
#     print('key_Sym' + str(i) + ' =', '0x%X' % (0xC003F + i + 1))

# 生成self.__Events语句
# i = 0xC0000
# while i <= 0xC006F:
#     if i == 0xC0000:
#         print('self.__Events = {', end='')
#     print('0x%X' % (i | 0xB1000) + ': [], ', end='')
#     print('0x%X' % (i | 0xB2000) + ': [], ', end='')
#     print('0x%X' % (i | 0xB3000) + ': [], ', end='')
#     if i == 0xC006F:
#         print('}', end='')
#     i += 1

from source.core.assembly.IOEvent import IOEvent3
import sys

print('IOEvent3占字节数', sys.getsizeof(IOEvent3()))
print(0xA000E, 0xA0000)
print((100 << 6) + 0xA0000)
print((1 << 6) + 0xA000E)
print((2 << 6) + 0xA0000)
print((2 << 6) + 0xA000E)
print((3 << 6) + 0xA0000)
print((3 << 6) + 0xA000E)
