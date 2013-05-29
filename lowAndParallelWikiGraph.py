import networkx
import csv, sys, time
#import pp
from scoop import futures

prefix = "simple."
categoryLinksFile = prefix+"categoryToCategory.csv"
pageFile = prefix+"pageToCategory.csv"

#outFile = open(prefix + "medicineAndHealthPages.txt", "w")
#categoriesTarget = ["Category:Medicine", "Category:Health"]
outFile = open(prefix + "medicineAndHealthPages.txt", "w")
categoriesTarget = ["Category:Medicine", "Category:Health", "Category:Nature", "Category:Life", "Category:Science"]


if prefix == "simple.":
    topCategories = ["Category:Agriculture", "Category:Arts", "Category:Business", "Category:Chronology", "Category:Culture", "Category:Education", "Category:Environment", "Category:Geography", "Category:Health", "Category:History", "Category:Humanities", "Category:Language", "Category:Law", "Category:Life", "Category:Mathematics", "Category:Medicine", "Category:Nature", "Category:People", "Category:Politics", "Category:Science", "Category:Society", "Category:Sports", "Category:Technology"]

else:
    topCategories = ["Category:Agriculture", "Category:Arts", "Category:Belief", "Category:Business", "Category:Chronology", "Category:Culture", "Category:Education", "Category:Environment", "Category:Geography", "Category:Health", "Category:History", "Category:Humanities", "Category:Language", "Category:Law", "Category:Life", "Category:Mathematics", "Category:Medicine", "Category:Nature", "Category:People", "Category:Politics", "Category:Science", "Category:Society", "Category:Sports", "Category:Technology"]

#G=networkx.DiGraph()
G = networkx.Graph()

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

def process(methodIn):
 
    #page, mapPageCats, G, nodes, topCategories, categoriesTarget = methodIn
    page, mapPageCats = methodIn #, G, nodes, topCategories, categoriesTarget = methodIn


    #print "Page === ", page, " map = ", mapPageCats
    smallestDist = 100000
    chooseCats = []
    
    for cat in mapPageCats:
        if cat not in nodes:
            continue

        #path = networkx.single_source_shortest_path_length(G, cat)
        
        for tcat in topCategories:
            try:
                dist = networkx.shortest_path_length(G, source=cat, target=tcat)
            except networkx.NetworkXNoPath:
                continue
            except networkx.NetworkXError:
                continue

            if len(chooseCats) == 0:
                chooseCats = [tcat]
                smallestDist = dist
            
            elif dist < smallestDist:
                smallestDist = dist
                chooseCats = [tcat]

            elif dist == smallestDist:
                chooseCats.append(tcat)

    print "Final decision --- Page: ", page, " Category: ", chooseCats
    for chooseCat in chooseCats:
        if chooseCat in categoriesTarget:
            return page
    
    return None

if __name__ == "__main__":
    #js = pp.Server(ppservers=())
    
    #print "Starting pp with", job_server.get_ncpus(), "workers"
    start_time = time.time()

    page = ""
    cats = []
    counter = 0

    print "Generating categories for each page"
    with open(pageFile, 'rb') as f:
        reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_ALL, quotechar ='"', escapechar='\\', doublequote=False)

        inputs = []
        for row in reader:
            #process(row[0], row[1:], G, nodes)
            page = row[0]
            cats = row[1:]

            counter += 1
            print "Processing line " , counter

            input = (page, cats) # , G, nodes, topCategories, categoriesTarget)
            inputs.append(input)

            if (counter % 1000) == 0:
                jobs = list(futures.map(process, inputs))
                #jobs = [js.submit(process, (input,), (), ("networkx",)) for input in inputs]

                for page in jobs:
                    if page is not None:
                        outFile.write(page + '\n' )
                        outFile.flush()
                
                inputs = []
        
        
        #The rest of the pages
        jobs = list(futures.map(process, inputs))
        #jobs = js.submit(process, (inputs,))
        for page in jobs:
            if page is not None:
                outFile.write(page + '\n' )
                outFile.flush()    


