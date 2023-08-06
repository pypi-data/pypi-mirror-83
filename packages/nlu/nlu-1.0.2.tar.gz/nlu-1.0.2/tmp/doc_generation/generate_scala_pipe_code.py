# this runs after python code has been generated nd converts the py code to Scala code

# 1. Convert " to '
# 2. Add val in the beginning of each line that has a =
# 3. Add 'new' after each = which is NOT created .pretrained()
# 4. Remove \
# 5. Convert py arrays [] to scalla Array in pipe.setTages()
# 6 New Fit/Transform sufix
# 7. New imports

def convert_py_code_to_scala(py_pipe_code):
