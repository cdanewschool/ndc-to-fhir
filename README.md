National Drug Code Directory to FHIR Parser
===========

This python script parses drugs from the National Drug Code Directory into a series of files containing FHIR-JSON dumps for Medication, Substance and Organization resource types. It is maintained by the Parsons Institute for Information Mapping (PIIM) and funded through the Telemedicine & Advanced Technology Research Center (TATRC).

Dependencies
------------
- [NDCD](http://www.fda.gov/drugs/informationondrugs/ucm142438.htm)'s `product.txt` file at `/data/ndc/product.txt`
- [RxNORM](http://www.nlm.nih.gov/research/umls/rxnorm/docs/rxnormfiles.html)'s RXNCONSO.RRF file at `/data/rxnorm/rrf/RXNCONSO.RRF`

Run
------
`python parse.py`

Links
--------
+ [FHIR](http://www.hl7.org/implement/standards/fhir/)
+ [National Drug Code Directory](http://www.fda.gov/drugs/informationondrugs/ucm142438.htm)
+ [RxNORM](http://www.nlm.nih.gov/research/umls/rxnorm/docs/rxnormfiles.html)