#National Drug Code Directory to FHIR Parser#

This python script parses drugs from the [National Drug Code Directory](http://www.fda.gov/Drugs/InformationOnDrugs/ucm142438.htm) into a series of files containing JSON dumps for [Medication](http://www.hl7.org/implement/standards/fhir/medication.html), [Substance](http://www.hl7.org/implement/standards/fhir/substance.html) and [Organization](http://www.hl7.org/implement/standards/fhir/organization.html) FHIR resource types. It is maintained by the [Parsons Institute for Information Mapping (PIIM)](http://piim.newschool.edu) and funded through the [Telemedicine & Advanced Technology Research Center (TATRC)](http://www.tatrc.org/).

###Instructions###

####Download Databases####
- Move into the cloned repo and create a `data` directory
  - `cd [ndc-to-fhir install directory]`
  - `mkdir data && cd data`
- Download and unzip the [NDC](http://www.fda.gov/Drugs/InformationOnDrugs/ucm142438.htm) database
  - `curl -O http://www.fda.gov/downloads/Drugs/DevelopmentApprovalProcess/UCM070838.zip`
  - `unzip UCM070838.zip -d ndc`
- Download the [RxNorm database](https://www.nlm.nih.gov/research/umls/rxnorm/docs/rxnormfiles.html) manually
  *NOTE: you must have a UMLS user account and be logged-in; account creation requires manual approval and takes a day or so*
  - [http://download.nlm.nih.gov/umls/kss/rxnorm/RxNorm_full_08052013.zip](http://download.nlm.nih.gov/umls/kss/rxnorm/RxNorm_full_08052013.zip)
  - Move the zip file to `[ndc-to-fhir install directory]/data/` manually or via the command line:
  	- `mv [RxNorm download location] [ndc-to-fhir install directory]/data`
  - Unzip the package manually and rename to `rxnorm` or via the command line:
     - `unzip RxNorm_full_08052013.zip -d rxnorm`

####Run####
- `cd [ndc-to-fhir install directory]`
- `python parse.py`

###Troubleshooting###
 - `locale.Error: unsupported locale setting`
    - run `locale -a` to get locales supported by your system
    - edit the `locale.setlocale(locale.LC_ALL, 'en_US.utf8')` line in `parse.py` to match one of the supported locales