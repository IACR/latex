# Metadata requirements

The purpose of this document is to describe the metadata requirements
for a new journal (as of 2021). Conferences are outside the scope of
this discussion.  The primary purpose of metadata is to facilitate
browsing, search, and bibliometrics. Bibliometrics is primarily
concerned with classification, indexing, and ranking of articles,
authors, journals, institutions, etc.  An example is the REF (Research
Excellence Framework) in the UK that is used to assess the quality of
research, and allocate funding accordingly. A lot of the academic
reputation of an author, article, institution, or journal flows from
statistics about how they are cited, and for this purpose it is
important to have unique identifiers on these entities, and to identify
the entities correctly at the time of publication.

The publication of metadata is carried out through different workflows,
including crawling by consumers, reporting by the journal to indexing agencies,
and archiving. There is no single schema that works for everyone, but we
should be able to capture the raw elements that can be used in the different
workflows. As an example, when a DOI is registered,
There are multiple consumers of metadata about publications, and there
are multiple agencies that assign unique identifiers. 

## Recommendations:
For the TL;DR crowd, this section summarizes recommendations.

1. We should strongly recommend that author names are written in full as they appear on
   previous papers. If an author has used a middle initial, it should be included.
2. We should strongly recommend that authors include their ORCID ID. They are not required.
   A coauthor's ORCID ID can be found by searching at https://orcid.org/
3. We should strongly recommend that authors include the ROR ID of their affiliations. They
   can be found at https://ror.org/search
4. We should strongly recommend that authors include canonicalized institution names. As an
   example, University of Southern California is preferred to just USC, since the latter
   could be University of South Carolina.
5. Authors may specify author names in UTF-8 or TeX codes. They will be translated to UTF-8.
6. Titles and abstracts may include mathematics through the use of TeX. As of now, crossref
   accepts both TeX and MathML, but MathML may be preferred for export. Luckily there is a
   converter: [latex2mathml](https://pypi.org/project/latex2mathml/).

The list of metadata fields is as follows:
1. title
2. abstract
3. a list of affiliations (without duplicates). Each one should have
   - full name
   - ROR ID (optional)
   - department (optional)
   - country
3. a list of authors, in order determined by the authors themselves. There is no notion of
   corresponding author in the paper itself. Each author should have:
   - full name as usually written on previous publications by the author. (required)
   - surname (required)
   - affiliation indices (required, written as {1,3} to indicate which in the list of
     affiliations applies to that author.
   - ORCID ID (optional)
4. funding agencies (TBD). See [below](#grants)
5. bibliographic references. These will be extracted from the submitted BibTeX file. Each
   one should contain necessary fields in a BibTeX entry, but also:
   - DOI (optional, but strongly urged)
   - URL (optional)   

## Identifier Namespaces
Unique identifiers are typically associated with the following:

* journal: Most commonly the ISSN (International Standard Serial Number). These have
  two types for print and electronic  media. ISBN is assigned to books rather than
  journals. Various disciplines also use identifiers that are unique to their
  discipline (e.g., pubmed). Journals may be issued a DOI, but this is rare.
* journal volume and/or issue. These are ad hoc, and are dependent on the publisher.
  They used to reflect a bound periodical.
* article: these are now assigned DOIs. These are segmented, and a prefix is generally assigned
  to a journal which then assigns DOIs within their prefix.
* author: names are inadequate (they aren't unique and they can change).
  - ORCID IDs are relatively recent, but are rapidly gaining traction.
  - Clarivate assigns their own [ResearcherID](http://www.researcherid.com/#rid-for-researchers)
  - Scopus assigns their own [identifier](https://www.scopus.com/authid/detail.uri?authorId=7004055156)
  - arXiv also assigns a [unique ID](https://arxiv.org/help/author_identifiers) to authors, but
    those are intended only for tracking within arXiv.
* affiliation: 
  - ROR IDs ([Research Organization Registry](https://ror.org/)) identifies institutions at
    roughly the level of a university but not a department. ROR is a community effort organized
    by Crossref, the California Digital Library,  Datacite,
    [Digital science](https://www.digital-science.com/), and is led by a steering group. They have
    explicitly decided not to identify departments within institutions, which leaves a hole because
    some indexing agencies want to rate computer science departments against each other. This is
    difficult because some are joint with mathematics or informatics or EE, and some have sub-departments (e.g. CSAIL and LIDS at MIT)
  - GRID ID (now replaced by ROR)
  - ISNI (International Standard Name Identifier). Started by ISO. Seems irrelevant now.
  - Crossref assigns funding ids to organizations, which could be
    [grant agencies](https://api.crossref.org/funders/100000001) or employers
    like [universities](https://api.crossref.org/funders/501100000765).
  - Scopus assigns an [AF-ID](https://service.elsevier.com/app/answers/detail/a_id/11215/supporthub/scopus/) to affiliations of authors. So does Clarivate.
  - Wikidata (e.g., [IBM](https://www.wikidata.org/wiki/Q37156)). Note that Wikidata assigns
    IDs at a finer level than ROR: [CSAIL](https://www.wikidata.org/wiki/Q1354917) or
    [IBM Research](https://www.wikidata.org/wiki/Q3146518) under IBM.
* funding sources:
    This is the most vague, and will be deferred for now. The most promising advance in this area
    is the [Open Funder Registry](https://www.crossref.org/services/funder-registry/) but that
    data is distributed by an old-style RDF file. This is apparently used by Scopus.
    Funding organizations tend to have hierarchical organization, as in
    - National Science Foundation (NSF)
      - Computer and Information Science and Engineering (CISE)
        - Division of Computing and Communication Foundations (CCF)
          - Cyberinfrastructure for Sustained Scientific Innovation (CSSI)
    Within these organizations, grants may also be assigned an identifier. Exactly how a funding
    agency gets cited varies from one to another. A document from ORCID
    [surveyed this topic](https://info.orcid.org/wp-content/uploads/2021/01/20161031-OrgIDProviderSurvey.pdf) in 2016, and listed the following:
    * Open Funder Registry (crossref?) See [CISE](https://api.crossref.org/funders/100000083) which
      is identified by 100000083. This seems most viable.
    * ISNI
    * Ringgold
    * Publisher Solutions International
    * GRID
    * LEI
    * OrgRef
    
       
## DOI creations

DOIs are issued by agencies delegated by doi.org. Two prominent
agencies are
[datacite](https://support.datacite.org/docs/api-create-dois) and
crossref.

## Indexing agencies

There are a large number of agencies who collect and organize
bibliographic information. Some of them are community-driven (e.g.,
crossref.org), and some are proprietary (e.g., Google and
Scopus). Funding agencies and research institutions also like to keep track
of what their organizations have contributed to, so that they can gain support from
taxpayers or stockholders. This section will summarize what I see as some of the most
important indexing agencies, but this list may change over time.

### Google Scholar

### crossref.org
Crossref maintains an [api](https://www.crossref.org/documentation/content-registration/) for
DOI assignment.

### Datacite
They publish a [schema](https://schema.datacite.org/) for metadata.

### DOAJ

### DBLP (computer science only)

### JATS

### Openaire

### Sherpa Romeo

### OpenDOAR

### Scopus (Elsevier)

### ISI Web of Science (clarivate)

## Export formats

### JATS
### meta tags in html files
### PDF metadata
### XML Formats

