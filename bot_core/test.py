
#
# def m(func):
#     def wrapper(func):
#         print(1)
#         result = func()
#         print(3)
#         return result
#     return wrapper
# @m
# def p(q):
#     print(q)
#
# p(1234)
#
class Message:
    a = 1
    b = 2

    def func(self):
        self.a = 3



message = Message()

print(message)














