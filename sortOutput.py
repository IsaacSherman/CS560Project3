import auxilliary as aux


translator = aux.loadInToTitleTranslator()
with open('isaac_sortedOutput.txt', 'r') as fin:
    results = []

    for line in fin:
        tup, list = line.split("|:")
        index, pr = tup.split(",")
        results.append((index, pr))

results = sorted(results, key = lambda x: -1*float(x[1]))


with open("sorted_out.txt", 'w', encoding='utf8') as fout:
    for tup in results:
        fout.write(translator[int(tup[0])]+"\t" + str(tup[1]) + "\n")
