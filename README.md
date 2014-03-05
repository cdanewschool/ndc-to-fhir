#National Drug Code Directory to FHIR Parser#

**ndc-to-fhir** is a Python script that parses drugs from the [National Drug Code Directory](http://www.fda.gov/Drugs/InformationOnDrugs/ucm142438.htm) into a series of [FHIR](http://www.hl7.org/implement/standards/fhir/)-JSON dumps ([Medication](http://www.hl7.org/implement/standards/fhir/medication.html), [Substance](http://www.hl7.org/implement/standards/fhir/substance.html) and [Organization](http://www.hl7.org/implement/standards/fhir/organization.html)). 

It is maintained by the [Parsons Institute for Information Mapping (PIIM)](http://piim.newschool.edu) and funded through the [Telemedicine & Advanced Technology Research Center (TATRC)](http://www.tatrc.org/).

###Requirements###
Python 2.5 or greater

###Instructions###

####Download Database####
- Move into the cloned repo and create a `data` directory
  - `cd [ndc-to-fhir install directory]`
  - `mkdir data && cd data`
- Download and unzip the [NDC](http://www.fda.gov/Drugs/InformationOnDrugs/ucm142438.htm) database
  - `curl -O http://www.fda.gov/downloads/Drugs/DevelopmentApprovalProcess/UCM070838.zip`
  - `unzip UCM070838.zip -d ndc`

####Run####
- `cd [ndc-to-fhir install directory]`
- `python parse.py`

####Troubleshooting####
 - `locale.Error: unsupported locale setting`
    - run `locale -a` to get locales supported by your system
    - edit the `locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')` line in `parse.py` to match one of the supported locales listed