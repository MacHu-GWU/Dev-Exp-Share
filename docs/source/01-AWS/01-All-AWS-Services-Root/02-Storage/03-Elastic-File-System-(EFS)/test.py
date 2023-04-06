import os

here = os.path.dirname(os.path.abspath(__file__))
p_data_dir = os.path.join(here, "data")
if not os.path.exists(p_data_dir):
    os.mkdir(p_data_dir)

for i in range(100):
    print("working on {} ith file".format(i))
    p = os.path.join(p_data_dir, "{}.txt".format(str(i).zfill(7)))
    with open(p, "w") as f:
        content = "hello world!\n" * 1000000
        f.write(content)