from multiprocessing import Process
from os import system
from glob import glob

def exec():
    system("mkdir exports")
    drawio_files = glob("*.drawio")
    #system("rm exports/*.pdf")
    processes = list()
    for i in range(len(drawio_files)):
        name = drawio_files[i][:len(drawio_files[i])-7] + ".pdf"
        processes.append(Process(target= lambda: system(f'drawio --crop -x -o {name} {drawio_files[i]}')))
        processes[len(processes)-1].start()
    for p in processes:
        p.join()
    system("mv *.pdf exports/")

exec()
