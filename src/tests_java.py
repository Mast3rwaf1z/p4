from os import system, listdir, path
from time import perf_counter

image_path = "modules/fires/BigFires"

images = [file for file in listdir(image_path) if path.isfile(path.join(image_path, file))]
images.sort()
image_size = len(images)

old_sequential_times = list()
print(f'running {image_size} tests of algorithm in java sequentially:')
for image in images:
    pre = perf_counter()
    system(f'java -jar src.jar {path.join(image_path, image)} old_sequential >> /dev/null')
    post = perf_counter()
    old_sequential_times.append(post-pre)

old_parallel_times = list()
print(f'running {image_size} tests of algorithm in java in parallel:')
for image in images:
    pre = perf_counter()
    system(f'java -jar src.jar {path.join(image_path, image)} old_parallel >> /dev/null')
    post = perf_counter()
    old_parallel_times.append(post-pre)

python_sequential_times = list()
print(f'running {image_size} tests of algorithm in python sequentially:')
for image in images:
    pre = perf_counter()
    system(f'python fire_detection_subsystem.py {path.join(image_path, image)} rgb >> /dev/null')
    post = perf_counter()
    python_sequential_times.append(post-pre)

python_parallel_times = list()
print(f'running {image_size} tests of algorithm in python in parallel:')
for image in images:
    pre = perf_counter()
    system(f'python fire_detection_subsystem.py {path.join(image_path, image)} pool_rgb >> /dev/null')
    post = perf_counter()
    python_parallel_times.append(post-pre)

old_sequential_average = sum(old_sequential_times)/52
old_parallel_average = sum(old_parallel_times)/52
python_sequential_average = sum(python_sequential_times)/52
python_parallel_average = sum(python_parallel_times)/52
speedup_old = old_sequential_average/old_parallel_average
speedup_python = python_sequential_average/python_parallel_average

print("Execution times")
print(f'\tSequential algorithm in Java:     {old_sequential_average}')
print(f'\tParallel algorithm in Java:       {old_parallel_average}')
print(f'\tSequential algorithm in Python:   {python_sequential_average}')
print(f'\tParallel algorithm in Python:     {python_parallel_average}')
print(f'\tJava algorithm speedup:           {speedup_old}')
print(f'\tPython speedup:                   {speedup_python}')
