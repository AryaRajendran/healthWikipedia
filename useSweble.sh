
type="en"

#for f in $(ls wikiFiles/${type}Wiki/); do 
#    echo $f; 
#    cp wikiFiles/${type}Wiki/$f sweble/Simple_Page.wikitext ; 
#    cd sweble/; 
#    java -jar target/parser-test-1.0-SNAPSHOT.jar Simple_Page ; 
#    cd - ; 
#    cp sweble/Simple_Page.html wikiFiles/${type}Sweble/$f;  
#done

for f in $(ls wikiFiles/${type}Sweble); do
    root=$(echo $f | sed "s/\.${type}//" )
    echo $root
    python convertSweebleText.py wikiFiles/${type}Sweble/$f > wikiFiles/${type}TextSweble/$root.txt
done

