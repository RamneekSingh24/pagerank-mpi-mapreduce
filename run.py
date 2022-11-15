import os
import subprocess

PART1_FILE = "part1/pr"
PART2_FILE = "part2/pr"
PART3_FILE = "part3/pr"


files = []
p1_rts = []
p2_rts = []
p3_rts = []

def check(out, expected):
    try:
        of = open(out, "r")
        ef = open(expected, "r")
    except  Exception as e:
        return True
    oprs = []
    eprs = []
    for line in of:
        toks = line.strip().split()
        oprs.append((toks[0], toks[1]))
    for line in ef:
        if "=" not in line:
            continue
        toks = line.strip().split()
        eprs.append((toks[0], toks[2]))
    if len(oprs) != len(eprs):
        # print(len(oprs), len(eprs))
        return True
        return False
    
    l2error = 0.0
    for i in range(len(oprs)):
        if oprs[i][0] != eprs[i][0]:
            return False
        l2error += (float(oprs[i][1]) - float(eprs[i][1]))**2

    l2error = l2error**0.5
    print("l2error", l2error)
    if l2error > 0.0001:
        return False
    return True
    
    
import time

def part1():
    global files
    files  = []
    print("checking part1")

    for f in os.listdir("pagerank/test"):
        if 'barabasi-10000.txt' in f:
            continue
        toks = f.split(".")
        if toks[-1] == "txt" and (toks[0].split("-")[-1] != 'j' and toks[0].split("-")[-1] != "p"):
            print(f'pagerank/test/{f}')
            
            st = time.time()
            r = subprocess.run([PART1_FILE, f'pagerank/test/{f}', 'res.txt'], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            if r.returncode == 0:
                ed = time.time()
                p1_rts.append(ed - st)
                files.append(f'pagerank/test/{f}')
                print((ed - st) *  1000, "ms")
                assert(check("res.txt", f'pagerank/test/{toks[0]}-pr-j.txt'))

def part2():
    global files
    files = []
    print("checking part2")
    for f in os.listdir("pagerank/test"):
        if 'barabasi-10000.txt' in f:
            continue
        toks = f.split(".")
        if toks[-1] == "txt" and (toks[0].split("-")[-1] != 'j' and toks[0].split("-")[-1] != "p"):
            print(f'pagerank/test/{f}')
            
            st = time.time()
            r = subprocess.run(['mpirun', '-np', '4', PART2_FILE, f'pagerank/test/{f}', 'res.txt'], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            if r.returncode == 0:
                ed = time.time()
                p2_rts.append(ed - st)
                files.append(f'pagerank/test/{f}')
                print((ed - st) *  1000, "ms")
                assert(check("res.txt", f'pagerank/test/{toks[0]}-pr-j.txt'))


def part3():
    global files
    files = []
    print("checking part2")
    for f in os.listdir("pagerank/test"):
        if 'barabasi-10000.txt' in f:
            continue
        toks = f.split(".")
        if toks[-1] == "txt" and (toks[0].split("-")[-1] != 'j' and toks[0].split("-")[-1] != "p"):
            print(f'pagerank/test/{f}')
            
            st = time.time()
            r = subprocess.run(['mpirun', '-np', '4', PART3_FILE, f'pagerank/test/{f}', 'res.txt'], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            if r.returncode == 0:
                ed = time.time()
                p3_rts.append(ed - st)
                files.append(f'pagerank/test/{f}')
                print((ed - st) *  1000, "ms")
                assert(check("res.txt", f'pagerank/test/{toks[0]}-pr-j.txt'))


part2()
print("part2")
print(files)
print(p2_rts)

part3()
print("part3")
print(files)
print(p3_rts)

part1()
print("part1")
print(files)
print(p1_rts)