National Drug Code Directory to FHIR Parser
===========

This python script parses drugs from the National Drug Code Directory into a series of files containing FHIR-JSON dumps for Medication, Substance and Organization resource types.

Dependencies
------------
- [NDCD](http://www.fda.gov/drugs/informationondrugs/ucm142438.htm)'s `product.txt` file at `/src-data/ndc/product.txt`
- [RxNORM](http://www.nlm.nih.gov/research/umls/rxnorm/docs/rxnormfiles.html)'s RXNCONSO.RRF file at `/src-data/rxnorm/rrf/RXNCONSO.RRF`

Run
---
`python parse.py`