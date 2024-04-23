import numba.cuda as cuda

print(cuda.is_available())
print(cuda.detect())
print(cuda.get_current_device())

# q: how can i can i calculate on the gpu?
# a: use numba.cuda.jit

# q: how can i make a class run on the gpu?
# a: use numba.cuda.jitclass

# q: how can i make a function run on the gpu?
# a: use numba.cuda.jit

# q: how can i make a function in a class run on the gpu?
# a: use numba.cuda.jit
