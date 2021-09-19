import json
import urllib.request

Authors = []
Orcid = []
ROR = []
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
  
    i = 0
    for a in Affiliation:
      ROR.append("")
      # Extract the ROR ID if present
      if "https://ror.org/" in a:
        split = a.split("https://ror.org/")
        ROR[i] = "https://api.ror.org/organizations/" + split[1]
        Affiliation[i] = split[0]
      i = i + 1

f.close()

i = 0
for a in Authors:
  print ("Author" + str(i) + ":")
  print ("  Name: " + a)
  print ("  Orcid: " + Orcid[i])
  print ("  Affiliation(s): ")
  for index in affindex[i]:
    ror = ROR[int(index)-1]
    print ("    " + Affiliation[int(index)-1])
    print ("    ROR: " + ror)
    if ror != "":
      with urllib.request.urlopen(ror) as url:
        data = json.loads(url.read().decode("utf-8"))
        print("      Retrieved name from ROR: " + data["name"])
  i = i+1



