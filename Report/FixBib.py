output = "Alles.bib"
paths = ["MyBibliography.bib"]







#####################################
## No need to edit below this line ##
#####################################

def clean_up(s):
    """
    Removes naughty characters.
    """
    naughty = [":",".","-","{","}", "\\", '"', "'", "`", "$",',',' ','\n','backslash']
    
    for n in naughty: s = s.replace(n,"")

    return s

def find_first(s, a=[' ', '-', ',', '}']):
    """
    Finds the first instance of any supplied character.
    """
    i = len(s)
    for c in a:
        j = s.find(c)
        if j >= 0 and j < i: i = j
    return i


# master list of keys to avoid duplicates
keys = []

# master file 
f_alles = open(output, 'w')

for path in paths:
    
    # read the contents    
    f = open(path, 'r')
    articles = f.read().split("@")
    f.close()
    
    #f = open(path, 'w')
    for n in range(1,len(articles)): 
        
        a = articles[n]        
        
        # get the name
        i  = a.find("\nauthor")
        i += a[i:].find("{") + 1
        j  = find_first(a[i:])
        name = a[i:j+i]
        
        # get the year
        i  = a.find("\nyear")
        i += a[i:].find("{") + 1
        j  = find_first(a[i:])
        year = a[i:j+i]
        
        # get the title word
        i  = a.find("\ntitle")
        i += a[i:].find("{") + 1
        j  = find_first(a[i:])
        title = a[i:j+i]
        
        # see if it's arxiv
        arxiv = ''
        if(a.find('\narxivId')>=0): arxiv='arxiv'
        
        
        # get the key name
        key = clean_up(arxiv+name+year+title)
    
        # insert the new key in the original file
        i = a.find("{")
        j = a.find(",")+1
        s = "@"+a[0:i]+"{"+key+","+a[j:]
        #f.write(s)

	# now if it's a new key, put it in the master file
        if not key in keys:

            # don't forget we saw it!
            keys.append(key)

            # output to the master file
            f_alles.write(s)

        # print something
        else: print "Duplicate key: "+key
    
    #f.close()

f_alles.close()




raw_input("Done! <enter>")
