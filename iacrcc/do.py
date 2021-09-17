

Authors = []
Orcid = []
affindex = [[]]
Affiliation = []

f = open("example.json", "r")
for line in f:
  if line.startswith("title: "):
    title = line.replace("title: ", "", 1).strip()
  elif line.startswith("authors: "):
    authors = line.replace("authors: ", "", 1).strip()
    Authors = authors.split(" : ")

    i = 0
    for a in Authors:
      Orcid.append("")
      affindex.append([])

      # Extract the Orcid ID if present
      if "https://orcid.org/" in a:
        split = a.split("https://orcid.org/")
        Orcid[i] = "https://orcid.org/" + split[1]
      
      # Determine to which affiliation the authors belongs
      if "\\unskip" in a:
        aff = a.split("\\unskip")
        Authors[i] = aff[0]
        if "https://orcid.org/" in aff[1]:
          ind = aff[1].split("https://orcid.org/")[0]
        else:
          ind = aff[1]
        ind = ind.replace("^", "")
        ind = ind.replace("{", "")
        ind = ind.replace("}", "")
        ind = ind.replace("$", "")
        Ind = ind.split(",")
        affindex[i] = Ind
      else:
        print ("Author " + a + " does not use \inst{}")

      i = i+1

  elif line.startswith("affiliation: "):
    affiliation = line.replace("affiliation: ", "", 1).strip()
    Affiliation = affiliation.split(" : ")

f.close()

i = 0
for a in Authors:
  print ("Author" + str(i) + ":")
  print ("  Name: " + a)
  print ("  Orcid: " + Orcid[i])
  print ("  Affiliation(s): ")
  for index in affindex[i]:
    print (Affiliation[int(index)-1])
  i = i+1



