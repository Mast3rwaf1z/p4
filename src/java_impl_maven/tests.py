from os import system, listdir, path
from time import perf_counter

image_path = "modules/fires"

images = [file for file in listdir(image_path) if path.isfile(path.join(image_path, file))]
images.sort()
print(images)
print("running 52 tests sequentially:")
sequential_times = list()
for image in images:
    pre = perf_counter()
    system(f'java -jar java_impl_maven/java_impl_maven.jar {path.join(image_path, image)} sequential')
    post = perf_counter()
    sequential_times.append(post-pre)

parallel_times = list()
print("running 52 tests in parallel:")
for image in images:
    pre = perf_counter()
    system(f'java -jar java_impl_maven/java_impl_maven.jar {path.join(image_path, image)} parallel')
    post = perf_counter()
    parallel_times.append(post-pre)

sequential_average = sum(sequential_times)/52
parallel_average = sum(parallel_times)/52
speedup = sequential_average/parallel_average

print(f'\tSequential execution time:    {sequential_average}')
print(f'\tParallel execution time:      {parallel_average}')
print(f'\tSpeedup:                      {speedup}')
