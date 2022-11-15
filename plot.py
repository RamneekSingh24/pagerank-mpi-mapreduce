import matplotlib.pyplot as plt

print("part2")
files = ['pagerank/test/barabasi-100000.txt', 'pagerank/test/java-org.txt', 'pagerank/test/erdos-90000.txt', 'pagerank/test/erdos.txt', 'pagerank/test/all-tests.txt', 'pagerank/test/frucht.txt', 'pagerank/test/icosahedral.txt', 'pagerank/test/levi.txt', 'pagerank/test/smallestcyclicgroup.txt', 'pagerank/test/coxeter.txt', 'pagerank/test/heawood.txt', 'pagerank/test/chvatal.txt', 'pagerank/test/erdos-20000.txt', 'pagerank/test/barabasi.txt', 'pagerank/test/nonline.txt', 'pagerank/test/herschel.txt', 'pagerank/test/octahedral.txt', 'pagerank/test/tetrahedral.txt', 'pagerank/test/barabasi-90000.txt', 'pagerank/test/java-tests.txt', 'pagerank/test/barabasi-20000.txt', 'pagerank/test/barabasi-80000.txt', 'pagerank/test/barabasi-50000.txt', 'pagerank/test/ring.txt', 'pagerank/test/erdos-60000.txt', 'pagerank/test/erdos-30000.txt', 'pagerank/test/cubical.txt', 'pagerank/test/tutte.txt', 'pagerank/test/thomassen.txt', 'pagerank/test/noperfectmatching.txt', 'pagerank/test/barabasi-60000.txt', 'pagerank/test/erdos-70000.txt', 'pagerank/test/erdos-50000.txt', 'pagerank/test/erdos-40000.txt', 'pagerank/test/diamond.txt', 'pagerank/test/bull.txt', 'pagerank/test/housex.txt', 'pagerank/test/barabasi-40000.txt', 'pagerank/test/folkman.txt', 'pagerank/test/grotzsch.txt', 'pagerank/test/erdos-100000.txt', 'pagerank/test/meredith.txt', 'pagerank/test/robertson.txt', 'pagerank/test/erdos-80000.txt', 'pagerank/test/erdos-10000.txt', 'pagerank/test/barabasi-30000.txt', 'pagerank/test/uniquely3colorable.txt', 'pagerank/test/petersen.txt', 'pagerank/test/famous.txt', 'pagerank/test/house.txt', 'pagerank/test/java.txt', 'pagerank/test/zachary.txt', 'pagerank/test/walther.txt', 'pagerank/test/krackhardt_kite.txt', 'pagerank/test/dodecahedral.txt', 'pagerank/test/barabasi-70000.txt', 'pagerank/test/franklin.txt', 'pagerank/test/mcgee.txt']
rts = [1.7481224536895752, 1.590127944946289, 1.3332295417785645, 0.3868672847747803, 0.35274767875671387, 0.36800479888916016, 0.3879227638244629, 0.40997982025146484, 0.39159059524536133, 0.3887972831726074, 0.37601447105407715, 0.3743412494659424, 0.6011693477630615, 0.3728611469268799, 0.4020078182220459, 0.384981632232666, 0.3932802677154541, 0.3674886226654053, 1.4706063270568848, 0.4202601909637451, 0.6114706993103027, 1.3370261192321777, 1.1219332218170166, 0.4080016613006592, 1.0450775623321533, 0.7311568260192871, 0.3765232563018799, 0.37433815002441406, 0.36917614936828613, 0.3509707450866699, 1.101525068283081, 1.231865644454956, 1.0604205131530762, 0.8404653072357178, 0.35913825035095215, 0.3723442554473877, 0.3899359703063965, 0.8382160663604736, 0.38675975799560547, 0.37429237365722656, 1.4176995754241943, 0.4316699504852295, 0.39057016372680664, 1.3036668300628662, 0.5569055080413818, 0.8041591644287109, 0.39148688316345215, 0.3710634708404541, 0.3612854480743408, 0.3797595500946045, 1.5782623291015625, 0.4206054210662842, 0.3707902431488037, 0.38147926330566406, 0.36565423011779785, 1.364819049835205, 0.4360487461090088, 0.3738682270050049]
files = [file.split('/')[-1].split(".")[0] for file in files]
rt_files = list(zip(rts, files))
rt_files.sort(key=lambda x: x[0])
rt_files = rt_files[30:]

plt.tight_layout()

plt.plot([i for i in range(len(rt_files))] , [x[0] for x in rt_files])
plt.xticks([i for i in range(len(rt_files))], [x[1] for x in rt_files], rotation=90, fontsize=8)
plt.ylabel('runtime (s)')   
# plt.figure(figsize=(2,2))
plt.tight_layout()
plt.savefig('part2.png', dpi=300)

plt.clf()

print("part3")

files = ['pagerank/test/barabasi-100000.txt', 'pagerank/test/java-org.txt', 'pagerank/test/erdos-90000.txt', 'pagerank/test/erdos.txt', 'pagerank/test/all-tests.txt', 'pagerank/test/frucht.txt', 'pagerank/test/icosahedral.txt', 'pagerank/test/levi.txt', 'pagerank/test/smallestcyclicgroup.txt', 'pagerank/test/coxeter.txt', 'pagerank/test/heawood.txt', 'pagerank/test/chvatal.txt', 'pagerank/test/erdos-20000.txt', 'pagerank/test/barabasi.txt', 'pagerank/test/nonline.txt', 'pagerank/test/herschel.txt', 'pagerank/test/octahedral.txt', 'pagerank/test/tetrahedral.txt', 'pagerank/test/barabasi-90000.txt', 'pagerank/test/java-tests.txt', 'pagerank/test/barabasi-20000.txt', 'pagerank/test/barabasi-80000.txt', 'pagerank/test/barabasi-50000.txt', 'pagerank/test/ring.txt', 'pagerank/test/erdos-60000.txt', 'pagerank/test/erdos-30000.txt', 'pagerank/test/cubical.txt', 'pagerank/test/tutte.txt', 'pagerank/test/thomassen.txt', 'pagerank/test/noperfectmatching.txt', 'pagerank/test/barabasi-60000.txt', 'pagerank/test/erdos-70000.txt', 'pagerank/test/erdos-50000.txt', 'pagerank/test/erdos-40000.txt', 'pagerank/test/diamond.txt', 'pagerank/test/bull.txt', 'pagerank/test/housex.txt', 'pagerank/test/barabasi-40000.txt', 'pagerank/test/folkman.txt', 'pagerank/test/grotzsch.txt', 'pagerank/test/erdos-100000.txt', 'pagerank/test/meredith.txt', 'pagerank/test/robertson.txt', 'pagerank/test/erdos-80000.txt', 'pagerank/test/erdos-10000.txt', 'pagerank/test/barabasi-30000.txt', 'pagerank/test/uniquely3colorable.txt', 'pagerank/test/petersen.txt', 'pagerank/test/famous.txt', 'pagerank/test/house.txt', 'pagerank/test/java.txt', 'pagerank/test/zachary.txt', 'pagerank/test/walther.txt', 'pagerank/test/krackhardt_kite.txt', 'pagerank/test/dodecahedral.txt', 'pagerank/test/barabasi-70000.txt', 'pagerank/test/franklin.txt', 'pagerank/test/mcgee.txt']
rts = [2.000204086303711, 1.845543384552002, 1.6166889667510986, 0.41718053817749023, 0.4040348529815674, 0.5411949157714844, 0.5437641143798828, 0.672248125076294, 0.518779993057251, 0.5424163341522217, 0.713437557220459, 0.6639130115509033, 0.6733849048614502, 0.37890195846557617, 0.5658392906188965, 0.5335676670074463, 0.591346025466919, 0.5628964900970459, 2.004757881164551, 0.44176340103149414, 0.9824306964874268, 1.7773585319519043, 1.427258014678955, 0.4577038288116455, 1.1371982097625732, 0.8505783081054688, 0.6287214756011963, 0.6149632930755615, 0.7116837501525879, 0.6581571102142334, 1.4204115867614746, 1.261521816253662, 1.099782943725586, 0.9415864944458008, 0.5698251724243164, 0.5551314353942871, 0.5774590969085693, 1.0641558170318604, 0.6023142337799072, 0.4715886116027832, 1.541109323501587, 0.5883700847625732, 0.6741499900817871, 1.3507044315338135, 0.593095064163208, 1.1669507026672363, 0.5912938117980957, 0.5558862686157227, 0.41576480865478516, 0.6190588474273682, 1.7129631042480469, 0.4857923984527588, 0.5484137535095215, 0.7714018821716309, 0.6263124942779541, 1.6751086711883545, 0.7117166519165039, 0.7257695198059082]

files = [file.split('/')[-1].split(".")[0] for file in files]
rt_files = list(zip(rts, files))
rt_files.sort(key=lambda x: x[0])
rt_files = rt_files[30:]

plt.tight_layout()

plt.plot([i for i in range(len(rt_files))] , [x[0] for x in rt_files])
plt.xticks([i for i in range(len(rt_files))], [x[1] for x in rt_files], rotation=90, fontsize=8)
plt.ylabel('runtime (s)')   
# plt.figure(figsize=(2,2))
plt.tight_layout()
plt.savefig('part3.png', dpi=300)


plt.clf()

print("part1")
files = ['pagerank/test/barabasi-100000.txt', 'pagerank/test/java-org.txt', 'pagerank/test/erdos-90000.txt', 'pagerank/test/erdos.txt', 'pagerank/test/all-tests.txt', 'pagerank/test/frucht.txt', 'pagerank/test/icosahedral.txt', 'pagerank/test/levi.txt', 'pagerank/test/smallestcyclicgroup.txt', 'pagerank/test/coxeter.txt', 'pagerank/test/heawood.txt', 'pagerank/test/chvatal.txt', 'pagerank/test/erdos-20000.txt', 'pagerank/test/barabasi.txt', 'pagerank/test/nonline.txt', 'pagerank/test/herschel.txt', 'pagerank/test/octahedral.txt', 'pagerank/test/tetrahedral.txt', 'pagerank/test/barabasi-90000.txt', 'pagerank/test/java-tests.txt', 'pagerank/test/barabasi-20000.txt', 'pagerank/test/barabasi-80000.txt', 'pagerank/test/barabasi-50000.txt', 'pagerank/test/ring.txt', 'pagerank/test/erdos-60000.txt', 'pagerank/test/erdos-30000.txt', 'pagerank/test/cubical.txt', 'pagerank/test/tutte.txt', 'pagerank/test/thomassen.txt', 'pagerank/test/noperfectmatching.txt', 'pagerank/test/barabasi-60000.txt', 'pagerank/test/erdos-70000.txt', 'pagerank/test/erdos-50000.txt', 'pagerank/test/erdos-40000.txt', 'pagerank/test/diamond.txt', 'pagerank/test/bull.txt', 'pagerank/test/housex.txt', 'pagerank/test/barabasi-40000.txt', 'pagerank/test/folkman.txt', 'pagerank/test/grotzsch.txt', 'pagerank/test/erdos-100000.txt', 'pagerank/test/meredith.txt', 'pagerank/test/robertson.txt', 'pagerank/test/erdos-80000.txt', 'pagerank/test/erdos-10000.txt', 'pagerank/test/barabasi-30000.txt', 'pagerank/test/uniquely3colorable.txt', 'pagerank/test/petersen.txt', 'pagerank/test/famous.txt', 'pagerank/test/house.txt', 'pagerank/test/java.txt', 'pagerank/test/zachary.txt', 'pagerank/test/walther.txt', 'pagerank/test/krackhardt_kite.txt', 'pagerank/test/dodecahedral.txt', 'pagerank/test/barabasi-70000.txt', 'pagerank/test/franklin.txt', 'pagerank/test/mcgee.txt']
rts = [5.8501200675964355, 8.314889907836914, 1.6081211566925049, 0.0028481483459472656, 0.0019516944885253906, 0.005529642105102539, 0.03799080848693848, 0.08053469657897949, 0.07934927940368652, 0.08054542541503906, 0.08026838302612305, 0.10807156562805176, 0.40012049674987793, 0.0054721832275390625, 0.006761789321899414, 0.0724954605102539, 0.0806882381439209, 0.07957577705383301, 4.852431774139404, 0.0023343563079833984, 0.9546606540679932, 4.430860280990601, 2.4175074100494385, 0.00269317626953125, 1.0107524394989014, 0.48023009300231934, 0.005988359451293945, 0.015817642211914062, 0.09188222885131836, 0.0903158187866211, 2.832261323928833, 1.1698570251464844, 0.8312015533447266, 0.6588120460510254, 0.00499415397644043, 0.018253564834594727, 0.012566804885864258, 1.775862216949463, 0.006402492523193359, 0.04083871841430664, 1.7366399765014648, 0.007554531097412109, 0.050523996353149414, 1.3761730194091797, 0.1731421947479248, 1.4956507682800293, 0.004961729049682617, 0.12452054023742676, 0.004041194915771484, 0.010824441909790039, 8.310149669647217, 0.002524137496948242, 0.006249904632568359, 0.05509448051452637, 0.09167313575744629, 3.636146068572998, 0.007969379425048828, 0.035126447677612305]

files = [file.split('/')[-1].split(".")[0] for file in files]
rt_files = list(zip(rts, files))
rt_files.sort(key=lambda x: x[0])
rt_files = rt_files[30:]

plt.tight_layout()

plt.plot([i for i in range(len(rt_files))] , [x[0] for x in rt_files])
plt.xticks([i for i in range(len(rt_files))], [x[1] for x in rt_files], rotation=90, fontsize=8)
plt.ylabel('runtime (s)')   
# plt.figure(figsize=(2,2))
plt.tight_layout()
plt.savefig('part1.png', dpi=300)



print("comparison")

print("part2")
files = ['pagerank/test/barabasi-100000.txt', 'pagerank/test/java-org.txt', 'pagerank/test/erdos-90000.txt', 'pagerank/test/erdos.txt', 'pagerank/test/all-tests.txt', 'pagerank/test/frucht.txt', 'pagerank/test/icosahedral.txt', 'pagerank/test/levi.txt', 'pagerank/test/smallestcyclicgroup.txt', 'pagerank/test/coxeter.txt', 'pagerank/test/heawood.txt', 'pagerank/test/chvatal.txt', 'pagerank/test/erdos-20000.txt', 'pagerank/test/barabasi.txt', 'pagerank/test/nonline.txt', 'pagerank/test/herschel.txt', 'pagerank/test/octahedral.txt', 'pagerank/test/tetrahedral.txt', 'pagerank/test/barabasi-90000.txt', 'pagerank/test/java-tests.txt', 'pagerank/test/barabasi-20000.txt', 'pagerank/test/barabasi-80000.txt', 'pagerank/test/barabasi-50000.txt', 'pagerank/test/ring.txt', 'pagerank/test/erdos-60000.txt', 'pagerank/test/erdos-30000.txt', 'pagerank/test/cubical.txt', 'pagerank/test/tutte.txt', 'pagerank/test/thomassen.txt', 'pagerank/test/noperfectmatching.txt', 'pagerank/test/barabasi-60000.txt', 'pagerank/test/erdos-70000.txt', 'pagerank/test/erdos-50000.txt', 'pagerank/test/erdos-40000.txt', 'pagerank/test/diamond.txt', 'pagerank/test/bull.txt', 'pagerank/test/housex.txt', 'pagerank/test/barabasi-40000.txt', 'pagerank/test/folkman.txt', 'pagerank/test/grotzsch.txt', 'pagerank/test/erdos-100000.txt', 'pagerank/test/meredith.txt', 'pagerank/test/robertson.txt', 'pagerank/test/erdos-80000.txt', 'pagerank/test/erdos-10000.txt', 'pagerank/test/barabasi-30000.txt', 'pagerank/test/uniquely3colorable.txt', 'pagerank/test/petersen.txt', 'pagerank/test/famous.txt', 'pagerank/test/house.txt', 'pagerank/test/java.txt', 'pagerank/test/zachary.txt', 'pagerank/test/walther.txt', 'pagerank/test/krackhardt_kite.txt', 'pagerank/test/dodecahedral.txt', 'pagerank/test/barabasi-70000.txt', 'pagerank/test/franklin.txt', 'pagerank/test/mcgee.txt']
rts = [1.7481224536895752, 1.590127944946289, 1.3332295417785645, 0.3868672847747803, 0.35274767875671387, 0.36800479888916016, 0.3879227638244629, 0.40997982025146484, 0.39159059524536133, 0.3887972831726074, 0.37601447105407715, 0.3743412494659424, 0.6011693477630615, 0.3728611469268799, 0.4020078182220459, 0.384981632232666, 0.3932802677154541, 0.3674886226654053, 1.4706063270568848, 0.4202601909637451, 0.6114706993103027, 1.3370261192321777, 1.1219332218170166, 0.4080016613006592, 1.0450775623321533, 0.7311568260192871, 0.3765232563018799, 0.37433815002441406, 0.36917614936828613, 0.3509707450866699, 1.101525068283081, 1.231865644454956, 1.0604205131530762, 0.8404653072357178, 0.35913825035095215, 0.3723442554473877, 0.3899359703063965, 0.8382160663604736, 0.38675975799560547, 0.37429237365722656, 1.4176995754241943, 0.4316699504852295, 0.39057016372680664, 1.3036668300628662, 0.5569055080413818, 0.8041591644287109, 0.39148688316345215, 0.3710634708404541, 0.3612854480743408, 0.3797595500946045, 1.5782623291015625, 0.4206054210662842, 0.3707902431488037, 0.38147926330566406, 0.36565423011779785, 1.364819049835205, 0.4360487461090088, 0.3738682270050049]
files = [file.split('/')[-1].split(".")[0] for file in files]
rt_files = list(zip(rts, files))
rt_files.sort(key=lambda x: x[0])
rt_files = rt_files[30:]

plt.tight_layout()

plt.plot([i for i in range(len(rt_files))] , [x[0] for x in rt_files], label='part2')
plt.xticks([i for i in range(len(rt_files))], [x[1] for x in rt_files], rotation=90, fontsize=8)
plt.ylabel('runtime (s)')   
# plt.figure(figsize=(2,2))
plt.tight_layout()


print("part3")

files = ['pagerank/test/barabasi-100000.txt', 'pagerank/test/java-org.txt', 'pagerank/test/erdos-90000.txt', 'pagerank/test/erdos.txt', 'pagerank/test/all-tests.txt', 'pagerank/test/frucht.txt', 'pagerank/test/icosahedral.txt', 'pagerank/test/levi.txt', 'pagerank/test/smallestcyclicgroup.txt', 'pagerank/test/coxeter.txt', 'pagerank/test/heawood.txt', 'pagerank/test/chvatal.txt', 'pagerank/test/erdos-20000.txt', 'pagerank/test/barabasi.txt', 'pagerank/test/nonline.txt', 'pagerank/test/herschel.txt', 'pagerank/test/octahedral.txt', 'pagerank/test/tetrahedral.txt', 'pagerank/test/barabasi-90000.txt', 'pagerank/test/java-tests.txt', 'pagerank/test/barabasi-20000.txt', 'pagerank/test/barabasi-80000.txt', 'pagerank/test/barabasi-50000.txt', 'pagerank/test/ring.txt', 'pagerank/test/erdos-60000.txt', 'pagerank/test/erdos-30000.txt', 'pagerank/test/cubical.txt', 'pagerank/test/tutte.txt', 'pagerank/test/thomassen.txt', 'pagerank/test/noperfectmatching.txt', 'pagerank/test/barabasi-60000.txt', 'pagerank/test/erdos-70000.txt', 'pagerank/test/erdos-50000.txt', 'pagerank/test/erdos-40000.txt', 'pagerank/test/diamond.txt', 'pagerank/test/bull.txt', 'pagerank/test/housex.txt', 'pagerank/test/barabasi-40000.txt', 'pagerank/test/folkman.txt', 'pagerank/test/grotzsch.txt', 'pagerank/test/erdos-100000.txt', 'pagerank/test/meredith.txt', 'pagerank/test/robertson.txt', 'pagerank/test/erdos-80000.txt', 'pagerank/test/erdos-10000.txt', 'pagerank/test/barabasi-30000.txt', 'pagerank/test/uniquely3colorable.txt', 'pagerank/test/petersen.txt', 'pagerank/test/famous.txt', 'pagerank/test/house.txt', 'pagerank/test/java.txt', 'pagerank/test/zachary.txt', 'pagerank/test/walther.txt', 'pagerank/test/krackhardt_kite.txt', 'pagerank/test/dodecahedral.txt', 'pagerank/test/barabasi-70000.txt', 'pagerank/test/franklin.txt', 'pagerank/test/mcgee.txt']
rts = [2.000204086303711, 1.845543384552002, 1.6166889667510986, 0.41718053817749023, 0.4040348529815674, 0.5411949157714844, 0.5437641143798828, 0.672248125076294, 0.518779993057251, 0.5424163341522217, 0.713437557220459, 0.6639130115509033, 0.6733849048614502, 0.37890195846557617, 0.5658392906188965, 0.5335676670074463, 0.591346025466919, 0.5628964900970459, 2.004757881164551, 0.44176340103149414, 0.9824306964874268, 1.7773585319519043, 1.427258014678955, 0.4577038288116455, 1.1371982097625732, 0.8505783081054688, 0.6287214756011963, 0.6149632930755615, 0.7116837501525879, 0.6581571102142334, 1.4204115867614746, 1.261521816253662, 1.099782943725586, 0.9415864944458008, 0.5698251724243164, 0.5551314353942871, 0.5774590969085693, 1.0641558170318604, 0.6023142337799072, 0.4715886116027832, 1.541109323501587, 0.5883700847625732, 0.6741499900817871, 1.3507044315338135, 0.593095064163208, 1.1669507026672363, 0.5912938117980957, 0.5558862686157227, 0.41576480865478516, 0.6190588474273682, 1.7129631042480469, 0.4857923984527588, 0.5484137535095215, 0.7714018821716309, 0.6263124942779541, 1.6751086711883545, 0.7117166519165039, 0.7257695198059082]

files = [file.split('/')[-1].split(".")[0] for file in files]
rt_files = list(zip(rts, files))
rt_files.sort(key=lambda x: x[0])
rt_files = rt_files[30:]

plt.tight_layout()

plt.plot([i for i in range(len(rt_files))] , [x[0] for x in rt_files], label='part3')
plt.xticks([i for i in range(len(rt_files))], [x[1] for x in rt_files], rotation=90, fontsize=8)
plt.ylabel('runtime (s)')   
# plt.figure(figsize=(2,2))
plt.tight_layout()


print("part1")
files = ['pagerank/test/barabasi-100000.txt', 'pagerank/test/java-org.txt', 'pagerank/test/erdos-90000.txt', 'pagerank/test/erdos.txt', 'pagerank/test/all-tests.txt', 'pagerank/test/frucht.txt', 'pagerank/test/icosahedral.txt', 'pagerank/test/levi.txt', 'pagerank/test/smallestcyclicgroup.txt', 'pagerank/test/coxeter.txt', 'pagerank/test/heawood.txt', 'pagerank/test/chvatal.txt', 'pagerank/test/erdos-20000.txt', 'pagerank/test/barabasi.txt', 'pagerank/test/nonline.txt', 'pagerank/test/herschel.txt', 'pagerank/test/octahedral.txt', 'pagerank/test/tetrahedral.txt', 'pagerank/test/barabasi-90000.txt', 'pagerank/test/java-tests.txt', 'pagerank/test/barabasi-20000.txt', 'pagerank/test/barabasi-80000.txt', 'pagerank/test/barabasi-50000.txt', 'pagerank/test/ring.txt', 'pagerank/test/erdos-60000.txt', 'pagerank/test/erdos-30000.txt', 'pagerank/test/cubical.txt', 'pagerank/test/tutte.txt', 'pagerank/test/thomassen.txt', 'pagerank/test/noperfectmatching.txt', 'pagerank/test/barabasi-60000.txt', 'pagerank/test/erdos-70000.txt', 'pagerank/test/erdos-50000.txt', 'pagerank/test/erdos-40000.txt', 'pagerank/test/diamond.txt', 'pagerank/test/bull.txt', 'pagerank/test/housex.txt', 'pagerank/test/barabasi-40000.txt', 'pagerank/test/folkman.txt', 'pagerank/test/grotzsch.txt', 'pagerank/test/erdos-100000.txt', 'pagerank/test/meredith.txt', 'pagerank/test/robertson.txt', 'pagerank/test/erdos-80000.txt', 'pagerank/test/erdos-10000.txt', 'pagerank/test/barabasi-30000.txt', 'pagerank/test/uniquely3colorable.txt', 'pagerank/test/petersen.txt', 'pagerank/test/famous.txt', 'pagerank/test/house.txt', 'pagerank/test/java.txt', 'pagerank/test/zachary.txt', 'pagerank/test/walther.txt', 'pagerank/test/krackhardt_kite.txt', 'pagerank/test/dodecahedral.txt', 'pagerank/test/barabasi-70000.txt', 'pagerank/test/franklin.txt', 'pagerank/test/mcgee.txt']
rts = [5.8501200675964355, 8.314889907836914, 1.6081211566925049, 0.0028481483459472656, 0.0019516944885253906, 0.005529642105102539, 0.03799080848693848, 0.08053469657897949, 0.07934927940368652, 0.08054542541503906, 0.08026838302612305, 0.10807156562805176, 0.40012049674987793, 0.0054721832275390625, 0.006761789321899414, 0.0724954605102539, 0.0806882381439209, 0.07957577705383301, 4.852431774139404, 0.0023343563079833984, 0.9546606540679932, 4.430860280990601, 2.4175074100494385, 0.00269317626953125, 1.0107524394989014, 0.48023009300231934, 0.005988359451293945, 0.015817642211914062, 0.09188222885131836, 0.0903158187866211, 2.832261323928833, 1.1698570251464844, 0.8312015533447266, 0.6588120460510254, 0.00499415397644043, 0.018253564834594727, 0.012566804885864258, 1.775862216949463, 0.006402492523193359, 0.04083871841430664, 1.7366399765014648, 0.007554531097412109, 0.050523996353149414, 1.3761730194091797, 0.1731421947479248, 1.4956507682800293, 0.004961729049682617, 0.12452054023742676, 0.004041194915771484, 0.010824441909790039, 8.310149669647217, 0.002524137496948242, 0.006249904632568359, 0.05509448051452637, 0.09167313575744629, 3.636146068572998, 0.007969379425048828, 0.035126447677612305]

files = [file.split('/')[-1].split(".")[0] for file in files]
rt_files = list(zip(rts, files))
rt_files.sort(key=lambda x: x[0])
rt_files = rt_files[30:]

plt.tight_layout()

plt.plot([i for i in range(len(rt_files))] , [x[0] for x in rt_files], label="part1")
plt.xticks([i for i in range(len(rt_files))], [x[1] for x in rt_files], rotation=90, fontsize=8)
plt.ylabel('runtime (s)')   
# plt.figure(figsize=(2,2))
plt.legend()
plt.tight_layout()

plt.savefig('comparison', dpi=300)

