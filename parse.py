#!/usr/bin/python

import json
import re
import locale
import datetime
import uuid
import os.path
import sys

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# This file parses drugs from the  FDA's National Drug Code directory into a JSON file containing FHIR-formatted equivalents
# Though the use of RxNorm as a reference database is not essential here, it positions the script to support additional coding systems in the future
#
# Dependencies:
# 1. NDCD's product.txt file at /data/ndc/product.txt (http://www.fda.gov/drugs/informationondrugs/ucm142438.htm)
# 2. RxNORM's RXNCONSO.RRF file at /data/rxnorm/rrf/RXNCONSO.RRF (http://www.nlm.nih.gov/research/umls/rxnorm/docs/rxnormfiles.html)
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# get script start for calculating execution time
start = datetime.datetime.now()

# set locale for output number formatting
locale.setlocale(locale.LC_ALL, 'en_US.utf8')

# configure supported coding systems 
# (key should match a source vocabularly listed at http://www.nlm.nih.gov/research/umls/rxnorm/docs/2013/rxnorm_doco_full_2013-3.html#s3_0)
supported_sources = dict([("MTHSPL","http://www.fda.gov")]) #("SNOMEDCT_US","http://snomed.info/id")

# mapping of NDC dosage codes to snomed ids
# TODO: verify these are coded correctly, fill in missing values
snomed_dosage_codes = dict(
	[
			("AEROSOL","52262001"),
			("AEROSOL, FOAM","30843009"),
			("AEROSOL, METERED","420847003"),
			("AEROSOL, SPRAY","421606006"),
			("BAR, CHEWABLE","429885007"),
			("BEAD","421271006"),
			("CAPSULE","385049006"),
			("CAPSULE, COATED","427129005"),
			("CAPSULE, COATED PELLETS","420293008"),
			("CAPSULE, COATED, EXTENDED RELEASE","421338009"),
			("CAPSULE, DELAYED RELEASE","421027002"),
			("CAPSULE, DELAYED RELEASE PELLETS","420767002"),
			("CAPSULE, EXTENDED RELEASE","421618002"),
			("CAPSULE, GELATIN COATED","427129005"),
			("CAPSULE, LIQUID FILLED","385051005"),
			("CAPSULE, GELATIN COATED","385049006"),
			("CELLULAR SHEET","?"),
			("CLOTH","?"),
			("CONCENTRATE","?"),
			("CREAM","385099005"),
			("CREAM, AUGMENTED","385099005"),
			("CRYSTAL",""),
			("DISC",""),
			("DOUCHE","336764006"),
			("DRESSING",""),
			("ELIXIR",""),
			("EMULSION",""),
			("ENEMA","68343008"),
			("EXTRACT","?"),
			("FILM","420460001"),
			("FILM, EXTENDED RELEASE","421043009"),
			("FILM, SOLUBLE","420460001"),
			("FOR SOLUTION",""),
			("FOR SUSPENSION",""),
			("FOR SUSPENSION, EXTENDED RELEASE",""),
			("GAS","385217004"),
			("GEL","385100002"),
			("GEL, DENTIFRICE","385088008"),
			("GEL, METERED","421669002"),
			("GLOBULE","259580005"),
			("GRANULE","385043007"),
			("GRANULE, DELAYED RELEASE","385043007"),
			("GRANULE, EFFERVESCENT","385043007"),
			("GRANULE, FOR SOLUTION","385043007"),
			("GRANULE, FOR SUSPENSION","385043007"),
			("GUM, CHEWING","385080001"),
			("IMPLANT","385286003"),
			("INHALANT","426837007"),
			("INJECTABLE, LIPOSOMAL","421522002"),
			("INJECTION","385218009"),
			("INJECTION, EMULSION","385221006"),
			("INJECTION, LIPID COMPLEX",""),
			("INJECTION, POWDER, FOR SOLUTION","385231004"),
			("INJECTION, POWDER, FOR SUSPENSION","385230003"),
			("INJECTION, POWDER, LYOPHILIZED, FOR SOLUTION","385231004"),
			("INJECTION, POWDER, LYOPHILIZED, FOR SUSPENSION","385230003"),
			("INJECTION, POWDER, LYOPHILIZED, FOR SUSPENSION, EXTENDED RELEASE","385230003"),
			("INJECTION, SOLUTION","118431008"),
			("INJECTION, SOLUTION, CONCENTRATE","118431008"),
			("INJECTION, SUSPENSION","385220007"),
			("INJECTION, SUSPENSION, LIPOSOMAL","421522002"),
			("INSERT","421532009"),
			("INSERT, EXTENDED RELEASE","420385006"),
			("INTRAUTERINE DEVICE","442015005"),
			("IRRIGANT",""),
			("JELLY",""),
			("KIT","385256005"),
			("LINIMENT","63316001"),
			("LIPSTICK",""),
			("LIQUID","420699003"),
			("LOTION","17519006"),
			("LOTION, AUGMENTED","17519006"),
			("LOTION/SHAMPOO","385104006"),
			("LOZENGE","385087003"),
			("MOUTHWASH","70409003"),
			("OIL","421890007"),
			("OINTMENT","385101003"),
			("OINTMENT, AUGMENTED","385101003"),
			("PASTE","37937005"),
			("PASTE, DENTIFRICE","385039008"),
			("PASTILLE","421079001"),
			("PATCH","36875001"),
			("PATCH, EXTENDED RELEASE","36875001"),
			("PELLET","420768007"),
			("PELLETS, COATED, EXTENDED RELEASE","421999009"),
			("PILL","46992007"),
			("PLASTER",""),
			("POULTICE","385117009"),
			("POWDER","420828001"),
			("POWDER, FOR SOLUTION","420955009"),
			("POWDER, FOR SUSPENSION","421080003"),
			("POWDER, METERED","420828001"),
			("RING",""),
			("RINSE",""),
			("SALVE",""),
			("SHAMPOO","385104006"),
			("SHAMPOO, SUSPENSION","385104006"),
			("SOAP",""),
			("SOLUTION","77899000"),
			("SOLUTION, CONCENTRATE",""),
			("SOLUTION, FOR SLUSH",""),
			("SOLUTION, GEL FORMING / DROPS",""),
			("SOLUTION, GEL FORMING, EXTENDED RELEASE",""),
			("SOLUTION/ DROPS","385019009"),
			("SPONGE","421288004"),
			("SPRAY","421720008"),
			("SPRAY, METERED","426969004"),
			("SPRAY, SUSPENSION","421720008"),
			("STICK","11190007"),
			("SUPPOSITORY","385194003"),
			("SUSPENSION","7946007"),
			("SUSPENSION, EXTENDED RELEASE",""),
			("SUSPENSION/ DROPS",""),
			("SWAB","420401004"),
			("SYRUP","385032004"),
			("TABLET","421026006"),
			("TABLET, CHEWABLE","66076007"),
			("TABLET, COATED","421721007"),
			("TABLET, DELAYED RELEASE","421374000"),
			("TABLET, DELAYED RELEASE PARTICLES","421535006"),
			("TABLET, EFFERVESCENT","385058004"),
			("TABLET, EXTENDED RELEASE","420627008"),
			("TABLET, FILM COATED","385057009"),
			("TABLET, FILM COATED, EXTENDED RELEASE","385057009"),
			("TABLET, FOR SUSPENSION","421026006"),
			("TABLET, MULTILAYER","421026006"),
			("TABLET, MULTILAYER, EXTENDED RELEASE","420627008"),
			("TABLET, ORALLY DISINTEGRATING","421366001"),
			("TABLET, ORALLY DISINTEGRATING, DELAYED RELEASE","421366001"),
			("TABLET, SOLUBLE","385035002"),
			("TABLET, SUGAR COATED","?"),
			("TAPE",""),
			("TINCTURE","422186009"),
			("WAFER","257465009")
	]
)

medications = []
organizations = []
substances = []

substances_dict = {}
system_dict = {}
organization_dict = {}

numlines = 0

# parse supported sources from RxNORM database
try:
	input = open("data/rxnorm/rrf/RXNCONSO.RRF","r")
except IOError:
	print "Error finding `data/rxnorm/rrf/RXNCONSO.RRF`"
	print "Please download RxNorm database to `data/rxnorm/` from http://www.nlm.nih.gov/research/umls/rxnorm/docs/rxnormfiles.html"
	sys.exit()
	
for line in input.readlines():
	
	d = line.split("|")
	system = d[11]
	
	# if source is supported
	if system in supported_sources:
		code = d[13]
		system_dict[code] = supported_sources[system]
		numlines+=1

print "Parsed " + locale.format('%d',numlines,grouping=True) + " codes from RxNORM database..."

# begin parsing NDC product database
try:
	input = open("data/ndc/product.txt","r")
except IOError:
	print "Error finding `data/ndc/product.txt`"
	print "Please download National Drug Code Directory to `data/ndc/` from http://www.fda.gov/drugs/informationondrugs/ucm142438.htm"
	sys.exit()

output_medications = open("medication","w")
output_organizations = open("organization","w")
output_substances = open("substance","w")

lines = input.readlines()
numlines = len(lines)
#numlines = 20

print "Parsing " + locale.format('%d',numlines,grouping=True) + " drugs from NDC database..."

input.seek(0)

for l in range(numlines):
	
	# skip header
	if l == 0: 
		continue
	
	line = lines[l]
	
	d = line.split("\t")
	
	ndc = d[1]
	
	# is source is supported
	if ndc in system_dict:
		
		id = d[0]
		type = d[2]
		proprietary_name = d[3]
		proprietary_name_suffix = d[4]
		nonproprietary_name = d[5]
		dosage_form = d[6] 
		route = d[7]
		label = d[12]
		active_ingredients = d[13].split("; ")
		active_ingredient_strengths = d[14].split("; ")
		active_ingredient_units = d[15].split("; ")
		
		code_code = ndc
		code_system = system_dict[ndc]
		
		form_code = snomed_dosage_codes[dosage_form] if dosage_form in snomed_dosage_codes else {}
		
		# build full name
		name = proprietary_name
		name_parts = []
		
		if proprietary_name_suffix: 
			name_parts.append( proprietary_name_suffix )
		
		if route: 
			name_parts.append( route )
		
		name_full = name 
		if len(name_parts)>0:
			name_full = name + "(" + ") (".join(name_parts) + ")"
		
		# TODO: how can we figure out what's a "brand"?
		d = { 'code': code_code, 'form_code': form_code, 'is_brand': True,'name_full': name_full }
		
		id = uuid.uuid1()
		name = {"value":name}
		text = {"status": { "value":"generated" }, "div": "<div>" + name_full + "</div>"}
		code = {"coding": [ {"system":{"value":code_system},"code":{"value":code_code},"display":{"value":nonproprietary_name}}]}
		isBrand = {"value": d['is_brand']}
		kind = {"value": "product"}
		product = {"form":{"coding":[{"system":{"value":"http://snomed.info/id"},"code":{"value":form_code},"display":{"value":dosage_form}}]}} #if len(d['form_code']) is not 0 else {}
		
		utcnow = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
		
		# add record for organization
		# TODO: test for duplicates
		if label not in organization_dict:
			o_id = uuid.uuid1()
			o_name = {"value":label}
			o_text = {"status": { "value":"generated" }, "div": "<div>" + label + "</div>"}
			o_content = {"Organization":{"text":o_text,"name":o_name}}
			organizations.append( {"title":"Organization Version \"1\"","id":str(o_id),"updated":utcnow,"published":utcnow,"author":[{"name":""}],"content":o_content} )
			
			organization_dict[label] = 1
		
		# parse ingredients
		ingredients = []
		
		# make sure components of ingredient detail match up
		if len(active_ingredients) == len(active_ingredient_strengths) and len(active_ingredients) == len(active_ingredient_units):
			
			for i in range(len(active_ingredients)):
				
				if not active_ingredients[i]:
					continue
					
				i_id = uuid.uuid1()
				i_name = {"value":active_ingredients[i]}
				
				if active_ingredients[i] not in substances_dict:
					i_text = {"status": { "value":"generated" }, "div": "<div>" + active_ingredients[i] + "</div>"}
					i_quantity = {"value":active_ingredient_strengths[i],"units":active_ingredient_units[i],"system":"http://unitsofmeasure.org"}
					i_content = {"Substance":{"text":i_text,"name":i_name,"quantity":i_quantity}}
					
					substances.append( {"title":"Substance Version \"1\"","id":str(i_id),"updated":utcnow,"published":utcnow,"author":[{"name":""}],"content":i_content} )
					
					substances_dict[active_ingredients[i]] = 1
				
				n = active_ingredient_units[i].split("/")
				
				numerator_val = active_ingredient_strengths[i]
				numerator_units = n[0]
				
				denominator_parts = re.search( '([\d\.]*)(\w*)', n[1] )
				denominator_val = denominator_parts.group(1) if denominator_parts.group(1) else 1
				denominator_units = denominator_parts.group(2) if denominator_parts.group(2) else ""
				
				numerator = {"value":{"value":numerator_val},"units":{"value":numerator_units},"system":{"value":"http://unitsofmeasure.org"},"code":{"value":numerator_units}}
				denominator = {"value":{"value":denominator_val}}
				
				if denominator_units and denominator_parts.group(1) == 1:
					denominator_units = dosage_form
				
				if denominator_units:
					denominator["units"]  = {"value":denominator_units}
					denominator["system"]  = {"value":"http://unitsofmeasure.org"}
					denominator["code"]  = {"value":denominator_units}
				
				ingredients.append( {"item":{"type":"Substance","reference":{"value":"substance/@"+str(i_id)},"display":{"value":i_name}},"amount":{"numerator":numerator,"denominator":denominator} } )
			
			if len(ingredients)>0:
				product['ingredient'] = ingredients
			
		content = {"Medication":{"text":text,"name":name,"code":code,"isBrand":isBrand,"kind": kind,"product":product}}
		
		#TODO: title, id, author name,
		medications.append( {"title":"Medication Version \"1\"","id":str(id),"updated":utcnow,"published":utcnow,"author":[{"name":""}],"content":content} )

input.close()

utcnow = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

data = {"title":"Import data for resource type Medication","id":"","totalResults":str(len(medications)),"link":[{"href":"{{hostname}}","rel":"self"}],"updated":utcnow,"entry":medications}
output_medications.write("list="+json.dumps(data,False,True,True,True,None,4))
output_medications.close()
print "Parsed " + locale.format('%d',len(medications),grouping=True) + " medications to file '../medication' (" + str(datetime.datetime.now() - start) + ")"

data = {"title":"Import data for resource type Organization","id":"","totalResults":str(len(organizations)),"link":[{"href":"{{hostname}}","rel":"self"}],"updated":utcnow,"entry":organizations}
output_organizations.write("list="+json.dumps(data,False,True,True,True,None,4))
output_organizations.close()
print "Parsed " + locale.format('%d',len(organizations),grouping=True) + " organizations to file '../organization' (" + str(datetime.datetime.now() - start) + ")"

data = {"title":"Import data for resource type Substance","id":"","totalResults":str(len(substances)),"link":[{"href":"{{hostname}}","rel":"self"}],"updated":utcnow,"entry":substances}
output_substances.write("list="+json.dumps(data,False,True,True,True,None,4))
output_substances.close()
print "Parsed " + locale.format('%d',len(substances),grouping=True) + " substances to file '../substance' (" + str(datetime.datetime.now() - start) + ")"