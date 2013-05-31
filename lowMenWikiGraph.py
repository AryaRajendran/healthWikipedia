import networkx as nx
import csv
import sys

numberOfPages = 4458427 / 5
pagesCounter = 0
part = str(sys.argv[1])

prefix = "bla."
categoryLinksFile = prefix+"categoryToCategory.csv"
pageFile = prefix+"pageToCategory.csv"

#outFile = open(prefix + "medicineAndHealthPages.txt" + part, "w")
#categoriesTarget = ["Category:Medicine", "Category:Health"]

outFile = open(prefix + "medicineAndHealthPages.txt", "w")
categoriesTarget = ["Category:Medicine", "Category:Health"]


#TOP CATEGORIES FOR ENGLISH
#topCategories = ["Category:Agriculture", "Category:Arts", "Category:Belief", "Category:Business", "Category:Chronology", "Category:Culture", "Category:Education", "Category:Environment", "Category:Geography", "Category:Health", "Category:History", "Category:Humanities", "Category:Language", "Category:Law", "Category:Life", "Category:Mathematics", "Category:Medicine", "Category:Nature", "Category:People", "Category:Politics", "Category:Science", "Category:Society", "Category:Sports", "Category:Technology"]

#TOP CATEGORIES FOR SIMPLE
topCategories = ["Category:Agriculture", "Category:Arts", "Category:Business", "Category:Chronology", "Category:Culture", "Category:Education", "Category:Environment", "Category:Geography", "Category:Health", "Category:History", "Category:Humanities", "Category:Language", "Category:Law", "Category:Life", "Category:Mathematics", "Category:Medicine", "Category:Nature", "Category:People", "Category:Politics", "Category:Science", "Category:Society", "Category:Sports", "Category:Technology"]

#G=nx.DiGraph()
G=nx.Graph()

print "Reading category file"
with open(categoryLinksFile, 'rb') as f:
    reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_ALL, quotechar ='"', escapechar='\\', doublequote=False)
    for row in reader:
        G.add_node(row[0])
        for cat in row[1:]:
            G.add_node(cat)
            G.add_edge(row[0], cat)
            #G.add_edge(cat, row[0])

nodes = G.nodes()

#print "Floyd-Warshall"
#path = nx.all_pairs_dijkstra_path(G)
#path = nx.all_pairs_shortest_path_length(G)

#print G.nodes()
#print path


def process(page, mapPageCats):

    #print "PAge === ", page, " map = ", mapPageCats
    smallestDist = 100000
    chooseCats = set()
    
    for cat in mapPageCats:
        if cat not in nodes:
            continue

        #path = nx.single_source_shortest_path_length(G, cat)
        
        for tcat in topCategories:
            try:
                dist = nx.shortest_path_length(G, source=cat, target=tcat)
            except nx.NetworkXNoPath:
                continue
            except nx.NetworkXError:
                continue

            if len(chooseCats) == 0:
                chooseCats.clear()
                chooseCats.add(tcat)
                smallestDist = dist
            
            elif dist < smallestDist:
                smallestDist = dist
                chooseCats.clear()
                chooseCats.add(tcat)

            elif dist == smallestDist:
                chooseCats.add(tcat)

    print "Final decision --- Page: ", page, " Category: ", chooseCats
    for chooseCat in chooseCats:
        if chooseCat in categoriesTarget:
            outFile.write(page + '\n' )
            outFile.flush()
            break


print "Generating categories for each page"
with open(pageFile, 'rb') as f:
    reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_ALL, quotechar ='"', escapechar='\\', doublequote=False)
    
    #TODO: fix error where the category name ends with "
    for row in reader:
        
        print "Processed ", 100.0 * pagesCounter / numberOfPages
        pagesCounter += 1
        process(row[0], row[1:])

