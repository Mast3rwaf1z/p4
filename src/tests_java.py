from os import system, listdir, path
from time import perf_counter

image_path = "modules/fires"

images = [file for file in listdir(image_path) if path.isfile(path.join(image_path, file))]
images.sort()
print(images)
print("running 52 tests of improved java algorithm sequentially:")
sequential_times = list()
for image in images:
    pre = perf_counter()
    system(f'java -jar src.jar {path.join(image_path, image)} sequential >> /dev/null')
    post = perf_counter()
    sequential_times.append(post-pre)

parallel_times = list()
print("running 52 tests of improved java algorithm in parallel:")
for image in images:
    pre = perf_counter()
    system(f'java -jar src.jar {path.join(image_path, image)} parallel >> /dev/null')
    post = perf_counter()
    parallel_times.append(post-pre)

old_sequential_times = list()
print("running 52 tests of old algorithm in java sequentially:")
for image in images:
    pre = perf_counter()
    system(f'java -jar src.jar {path.join(image_path, image)} old_sequential >> /dev/null')
    post = perf_counter()
    old_sequential_times.append(post-pre)

old_parallel_times = list()
print("running 52 tests of old algorithm in java in parallel:")
for image in images:
    pre = perf_counter()
    system(f'java -jar src.jar {path.join(image_path, image)} old_parallel >> /dev/null')
    post = perf_counter()
    old_parallel_times.append(post-pre)

python_sequential_times = list()
print("running 52 tests of old algorithm in python sequentially:")
for image in images:
    pre = perf_counter()
    system(f'python fire_detection_subsystem.py {path.join(image_path, image)} rgb >> /dev/null')
    post = perf_counter()
    python_sequential_times.append(post-pre)

python_parallel_times = list()
print("running 52 tests of old algorithm in python in parallel:")
for image in images:
    pre = perf_counter()
    system(f'python fire_detection_subsystem.py {path.join(image_path, image)} pool_rgb >> /dev/null')
    post = perf_counter()
    python_parallel_times.append(post-pre)

sequential_average = sum(sequential_times)/52
parallel_average = sum(parallel_times)/52
old_sequential_average = sum(old_sequential_times)/52
old_parallel_average = sum(old_parallel_times)/52
python_sequential_average = sum(python_sequential_times)/52
python_parallel_average = sum(python_parallel_times)/52
speedup = sequential_average/parallel_average
speedup_old = old_sequential_average/old_parallel_average
speedup_python = python_sequential_average/python_parallel_average

print("Execution times")
print(f'\tNew sequential algorithm in Java:     {sequential_average}')
print(f'\tNew parallel algorithm in Java:       {parallel_average}')
print(f'\tOld sequential algorithm in Java:     {old_sequential_average}')
print(f'\tOld parallel algorithm in Java:       {old_parallel_average}')
print(f'\tOld sequential algorithm in Python:   {python_sequential_average}')
print(f'\tOld parallel algorithm in Python:     {python_parallel_average}')
print(f'\tNew Java algorithm speedup:           {speedup}')
print(f'\tOld Java algorithm speedup:           {speedup_old}')
print(f'\tOld Python speedup:                   {speedup_python}')
