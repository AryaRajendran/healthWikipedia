import networkx as nx
import csv

prefix = "small."
categoryLinksFile = prefix+"categoryToCategory.csv"
pageFile = prefix+"pageToCategory.csv"

topCategories = ["Category:Agriculture", "Category:Arts", "Category:Belief", "Category:Business", "Category:Chronology", "Category:Culture", "Category:Education", "Category:Environment", "Category:Geography", "Category:Health", "Category:History", "Category:Humanities", "Category:Language", "Category:Law", "Category:Life", "Category:Mathematics", "Category:Medicine", "Category:Nature", "Category:People", "Category:Politics", "Category:Science", "Category:Society", "Category:Sports", "Category:Technology"]
mapPageCat = {}

#G=nx.DiGraph()
G=nx.Graph()

print "Reading category file"
with open(categoryLinksFile, 'rb') as f:
    reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_ALL, quotechar ='"', escapechar='\\', doublequote=False)
    for row in reader:
        G.add_node(row[0])
        G.add_node(row[1])
        G.add_edge(row[0], row[1])
	    #G.add_edge(row[1], row[0])

print "Floyd-Warshall"
#path = nx.all_pairs_dijkstra_path(G)
path = all_pairs_shortest_path_length(G)

#print G.nodes()
#print path

print "Generating categories for each page"
with open(pageFile, 'rb') as f:
    reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_ALL, quotechar ='"', escapechar='\\', doublequote=False)
    
    for (page, cat) in reader:


        if cat not in path:
            #print "Page: ", row[0], " has category ", row[1], " which is not in paths map"
            continue

        for tcat in topCategories:
            

            if tcat in path[cat]:
                dist = int(path[cat][tcat])

                #print "Page ", page, " cat = ", cat, " catDest = ", tcat, " dist = ", dist
                if page not in mapPageCat:
                    mapPageCat[page] = (tcat, dist)
                
                else:
                    smallestDist = mapPageCat[page][1]

                    if dist < smallestDist:
                        mapPageCat[page] = (tcat, dist)



with open(prefix + "healthPages.txt", "w") as f:

    print "Printing Map:"
    for (k,v) in mapPageCat.iteritems():
        print "Page: ", k, " Category: ", v
        if v[0] == "Category:Health":
            f.write(k + '\n' )



