#!/usr/bin/env python
# Extract header information from a NetCDF file write to XML for importing into GeoNetwork.

# Claire Trenham, September 2014
# Last updated 15/10/2014

# Usuage: python CMIP5_nc_metadata_to_xml_geonetwork.py <path to input file>.nc

from netCDF4 import Dataset
import sys, os, datetime

#def extractn(fulllist,n):
#    itr=iter(fulllist)
#    while True:
#        yield tuple([itr.next() for i in range(n)])

file1=[]
if len(sys.argv)<2:
    sys.exit('Usage: %s /path/to/file.nc' % sys.argv[0])
print sys.argv[1]
file1.append(str(sys.argv[1]))

xmlfile=str(sys.argv[1][:-3]).split('/')[-1]+'_GN.xml'
if not os.path.exists(xmlfile):#(file1[0]):
    print 'Getting metadata...'
    realfile=os.path.realpath(file1[0])  #Get actual location of the file not symlink
    print 'True file path is '+realfile
    f=Dataset(realfile)  
    ncdims=f.dimensions
    ncvars=f.variables  # Get the variables
    ncglobattr=f.ncattrs()  #Get the global attributes

##The above three lines are really all you need: Now have everything to write out again, but let's do some stuff...
##Print dimensions
#for dims in f.dimensions:
#    print 'Dimension', dims
##Print variables
#for name in f.variables:
#    print 'Variable', name
##Print global attributes
#for name in f.ncattrs():
#    print 'Global attr', name#, '=', getattr(f,name)

#Get dimensions and arguments for the variables
    dimkeys=f.dimensions.keys()
    varkeys=f.variables.keys()
    varattrs=[]
    for i in range(len(ncvars)):
        varattrs.append(f.variables[varkeys[i]].ncattrs())  #eg timeattrs=f.variables['time'].ncattrs() 

    now=datetime.datetime.today().isoformat('T')


# Write to a text file for example.
    print 'Writing to text file...'
    outfile=str(sys.argv[1][:-3]).split('/')[0]+'_metadata.txt'
    print outfile
    wrfile=open(outfile,'w')

    wrfile.write('\n--- Dimensions : length ---\n') #>>> Dimensions : length <<<\n')
    for dims in range(len(ncdims)):
        wrfile.write(dimkeys[dims]+' : '+str(len(f.dimensions[dimkeys[dims]]))+'\n')

    wrfile.write('--- Variable - type, dimensions, shape ---\n') #>>> Variable - type, dimensions, shape <<<\n')
    wrfile.write('--- Variable : arguments : value ---\n') #>>> Variable : arguments : value <<<\n')
    for name in range(len(varkeys)):
        if not varattrs[name]:
            wrfile.write(varkeys[name]+' : '+'\n')
        else:
            wrfile.write(varkeys[name]+' - type: '+str(f.variables[varkeys[name]].dtype)+', dimensions: '+str(f.variables[varkeys[name]].dimensions)+', shape: '+str(f.variables[varkeys[name]].shape)+'\n')
        for args in range(len(varattrs[name])):
            wrfile.write(varkeys[name]+' : '+varattrs[name][args]+' : '+str(f.variables[varkeys[name]].getncattr(varattrs[name][args]))+'\n')

    wrfile.write('--- Global attribute : value ---\n') #>>> Global attribute : value <<<\n')
    for name in f.ncattrs():
        wrfile.write(name+' : '+str(getattr(f,name))+'\n')

    wrfile.close()

    absfile=outfile #This file contains the text we'll use as the abstract in the XML


# Write into XML for import into geonetwork
#    print 'Writing XML to ...'
    outfile=str(sys.argv[1][:-3]).split('/')[-1]+'_GN.xml'
#    print outfile
    wrfile=open(outfile,'w')
    abstext=open(absfile,'r')
    abstract=abstext.read()
    abstract=abstract.replace("&", "&amp;")
    abstract=abstract.replace(">", "&gt;")
    abstract=abstract.replace("<", "&lt;")
    model=str(getattr(f,'model_id'))
    expt=str(getattr(f,'experiment_id'))
    freq=str(getattr(f,'frequency'))
    realm=str(getattr(f,'modeling_realm'))
    rip=realfile.split('_')[-2]
    if freq=='fx':
        rip=realfile.split('_')[-1][:-3]
    dates=realfile.split('_')[-1][:-3]
    if freq=='fx':
        dates=''
#var=str(varkeys[-1])
#varcheck=realfile.split('_')[-6].split('/')[-1]
#if not var==varcheck:
#    print 'ERROR: Variable mismatch, check file and XML generation code'
    var=str(varkeys[varkeys.index(realfile.split('/')[-1].split('_')[0])]) #[-6]
#varlong=str(f.variables[varkeys[-1]].getncattr(varattrs[-1][varattrs[-1].index('long_name')]))
    varlong=str(f.variables[varkeys[varkeys.index(realfile.split('/')[-1].split('_')[0])]].getncattr(varattrs[varkeys.index(realfile.split('/')[-1].split('_')[0])][varattrs[varkeys.index(realfile.split('/')[-1].split('_')[0])].index('long_name')]))
#basedate=datetime.datetime.strptime(f.variables[varkeys[0]].getncattr(varattrs[0][varattrs[0].index('units')])[(f.variables[varkeys[0]].getncattr(varattrs[0][varattrs[0].index('units')])).index('e')+2:], "%Y-%m-%d")
#basedate=datetime.datetime.strptime(f.variables[varkeys[varkeys.index('time')]].getncattr(varattrs[varkeys.index('time')][varattrs[varkeys.index('time')].index('units')])[(f.variables[varkeys[varkeys.index('time')]].getncattr(varattrs[varkeys.index('time')][varattrs[varkeys.index('time')].index('units')])).index('e')+2:(f.variables[varkeys[varkeys.index('time')]].getncattr(varattrs[varkeys.index('time')][varattrs[varkeys.index('time')].index('units')])).index('e')+12], "%Y-%m-%d")
#basedate=datetime.datetime.strptime(f.variables[varkeys[varkeys.index('time')]].getncattr(varattrs[varkeys.index('time')][varattrs[varkeys.index('time')].index('units')])[(f.variables[varkeys[varkeys.index('time')]].getncattr(varattrs[varkeys.index('time')][varattrs[varkeys.index('time')].index('units')])).index('e')+2:][:10], "%Y-%m-%d")
# Undefined for 'fx'    basedate=datetime.datetime.strptime(str(f.variables[varkeys[varkeys.index('time')]].getncattr(varattrs[varkeys.index('time')][varattrs[varkeys.index('time')].index('units')])).split(' ')[2], "%Y-%m-%d")
    if hasattr(f,'source'): 
        sourcestr="Source: "+str(getattr(f,'source'))+"."
    else: sourcestr=""
    if hasattr(f,'contact'): 
        contactstr="\nContact: "+str(getattr(f,'contact'))
    else: contactstr=""
    if hasattr(f,'references'): 
        refstr="\nReferences: "+str(getattr(f,'references'))
    else: refstr=""
    lineage=sourcestr+contactstr+refstr
# Check for dimensions - handle global average data and time invariant data
    try: lats=f.dimensions['lat']
    except: 
	try: lats=f.dimensions['j']
	except: lats=[]
    try: lons=f.dimensions['lon']
    except: 
	try: lons=f.dimensions['i']
	except: lons=[]
    try: times=f.dimensions['time']
    except: times=[]
    try: levs=f.dimensions['lev']
    except: 
        try: levs=f.dimensions['plev']
        except: levs=[]
    if times: #+str(len(f.dimensions[dimkeys[0]]))
        try: [date1a, date1b, date1c]=(str(f.variables[varkeys[varkeys.index('time')]].getncattr(varattrs[varkeys.index('time')][varattrs[varkeys.index('time')].index('units')])).split(' ')[-1]).split('-')
	except: 
		try: [date1a, date1b, date1c]=(str(f.variables[varkeys[varkeys.index('time')]].getncattr(varattrs[varkeys.index('time')][varattrs[varkeys.index('time')].index('units')])).split(' ')[2]).split('-')
		except: [date1a, date1b, date1c]=(str(int(f.variables[varkeys[varkeys.index('time')]].getncattr(varattrs[varkeys.index('time')][varattrs[varkeys.index('time')].index('units')]).split(' ')[2].split('-')[0])+1)+'-'+'-'.join(f.variables[varkeys[varkeys.index('time')]].getncattr(varattrs[varkeys.index('time')][varattrs[varkeys.index('time')].index('units')]).split(' ')[2].split('-')[1:3])).split('-')
	#[date1a, date1b, date1c]=date1.split('-')
	date2=date1a.zfill(4)+'-'+date1b.zfill(2)+'-'+date1c.zfill(2)
	basedate=datetime.datetime.strptime(date2, "%Y-%m-%d")
	timedim='''			<gmd:axisDimensionProperties>
				<gmd:MD_Dimension>
					<gmd:dimensionName>
						<gmd:MD_DimensionNameTypeCode codeListValue="time" codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#MD_DimensionNameTypeCode"/>
					</gmd:dimensionName>
					<gmd:dimensionSize>
						<gco:Integer>'''+str(len(f.dimensions['time']))+'''</gco:Integer>
					</gmd:dimensionSize>
				</gmd:MD_Dimension>
			</gmd:axisDimensionProperties>'''
        timeextent='''			<gmd:extent>
				<gmd:EX_Extent>
					<gmd:temporalElement>
						<gmd:EX_TemporalExtent>
							<gmd:extent>
								<gml:TimePeriod gml:id="d19360e515a1052958">
									<gml:beginPosition>'''+datetime.datetime.isoformat(basedate+datetime.timedelta(days=f.variables['time'][0]))+'''</gml:beginPosition>
									<gml:endPosition>'''+datetime.datetime.isoformat(basedate+datetime.timedelta(days=f.variables['time'][-1]))+'''</gml:endPosition>
								</gml:TimePeriod>
							</gmd:extent>
						</gmd:EX_TemporalExtent>
					</gmd:temporalElement>
				</gmd:EX_Extent>
			</gmd:extent>'''
    else: 
        timedim=""
        timeextent=""
    if lats: #str(len(f.dimensions[dimkeys[1]]))
        try: latlen=str(len(f.dimensions['lat']))
        except: latlen=str(len(f.dimensions['j']))
        latdim='''			<gmd:axisDimensionProperties>
				<gmd:MD_Dimension>
					<gmd:dimensionName>
						<gmd:MD_DimensionNameTypeCode codeListValue="row" codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#MD_DimensionNameTypeCode"/>
					</gmd:dimensionName>
					<gmd:dimensionSize>
						<gco:Integer>'''+latlen+'''</gco:Integer>
					</gmd:dimensionSize>
				</gmd:MD_Dimension>
			</gmd:axisDimensionProperties>'''
        gridvec="grid"
        Sbound=str(f.variables[varkeys[varkeys.index('lat')]][:].min())
        Nbound=str(f.variables[varkeys[varkeys.index('lat')]][:].max())
    else: 
        latdim=""
        gridvec="vector"
        Sbound="-90"
        Nbound="90"
    if lons: #str(len(f.dimensions[dimkeys[2]]))
        try: lonlen=str(len(f.dimensions['lon']))
        except: lonlen=str(len(f.dimensions['i']))
        londim='''			<gmd:axisDimensionProperties>
				<gmd:MD_Dimension>
					<gmd:dimensionName>
						<gmd:MD_DimensionNameTypeCode codeListValue="column" codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#MD_DimensionNameTypeCode"/>
					</gmd:dimensionName>
					<gmd:dimensionSize>
						<gco:Integer>'''+lonlen+'''</gco:Integer>
					</gmd:dimensionSize>
				</gmd:MD_Dimension>
			</gmd:axisDimensionProperties>'''
        Wbound=str(f.variables[varkeys[varkeys.index('lon')]][:].min())
        Ebound=str(f.variables[varkeys[varkeys.index('lon')]][:].max())
    else: 
        londim=""
        Wbound="-180"
        Ebound="180"
    if levs:
        try: levlen=str(len(f.dimensions['lev']))
        except: levlen=str(len(f.dimensions['plev']))
        levdim='''			<gmd:axisDimensionProperties>
				<gmd:MD_Dimension>
					<gmd:dimensionName>
						<gmd:MD_DimensionNameTypeCode codeListValue="vertical" codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#MD_DimensionNameTypeCode"/>
					</gmd:dimensionName>
					<gmd:dimensionSize>
						<gco:Integer>'''+levlen+'''</gco:Integer>
					</gmd:dimensionSize>
				</gmd:MD_Dimension>
			</gmd:axisDimensionProperties>'''
    else: levdim=""
    try: creationDate=str(getattr(f,'creation_date'))
    except: creationDate=str(getattr(f,'history')[0:24])


# Write XML
    print 'Writing XML to ...'
    print outfile
    wrfile.write('''<?xml version="1.0" encoding="UTF-8"?>
<gmd:MD_Metadata xmlns:gco="http://www.isotc211.org/2005/gco" xmlns:gts="http://www.isotc211.org/2005/gts" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:gml="http://www.opengis.net/gml" xmlns:gmd="http://www.isotc211.org/2005/gmd" xsi:schemaLocation="http://www.isotc211.org/2005/gmd http://www.isotc211.org/2005/gmd/gmd.xsd http://www.isotc211.org/2005/srv http://schemas.opengis.net/iso/19139/20060504/srv/srv.xsd">
	<gmd:fileIdentifier>
                <gco:CharacterString>'''+os.readlink(file1[0])[8:]+'''</gco:CharacterString>
        </gmd:fileIdentifier>
        <gmd:language>
		<gmd:LanguageCode codeList="http://www.loc.gov/standards/iso639-2/" codeListValue="eng"/>
	</gmd:language>
	<gmd:characterSet>
		<gmd:MD_CharacterSetCode codeListValue="utf8" codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#MD_CharacterSetCode"/>
	</gmd:characterSet>
	<gmd:contact>
		<gmd:CI_ResponsibleParty>
			<gmd:individualName gco:nilReason="missing">
				<gco:CharacterString/>
			</gmd:individualName>
			<gmd:organisationName>
				<gco:CharacterString>NCI</gco:CharacterString>
			</gmd:organisationName>
			<gmd:positionName gco:nilReason="missing">
				<gco:CharacterString/>
			</gmd:positionName>
			<gmd:contactInfo>
				<gmd:CI_Contact>
					<gmd:phone>
						<gmd:CI_Telephone>
							<gmd:voice gco:nilReason="missing">
								<gco:CharacterString/>
							</gmd:voice>
							<gmd:facsimile gco:nilReason="missing">
								<gco:CharacterString/>
							</gmd:facsimile>
						</gmd:CI_Telephone>
					</gmd:phone>
					<gmd:address>
						<gmd:CI_Address>
							<gmd:deliveryPoint gco:nilReason="missing">
								<gco:CharacterString/>
							</gmd:deliveryPoint>
							<gmd:city gco:nilReason="missing">
								<gco:CharacterString/>
							</gmd:city>
							<gmd:administrativeArea gco:nilReason="missing">
								<gco:CharacterString/>
							</gmd:administrativeArea>
							<gmd:postalCode gco:nilReason="missing">
								<gco:CharacterString/>
							</gmd:postalCode>
							<gmd:country gco:nilReason="missing">
								<gco:CharacterString/>
							</gmd:country>
							<gmd:electronicMailAddress>
								<gco:CharacterString>esg_publishing@nf.nci.org.au</gco:CharacterString>
							</gmd:electronicMailAddress>
						</gmd:CI_Address>
					</gmd:address>
				</gmd:CI_Contact>
			</gmd:contactInfo>
			<gmd:role>
				<gmd:CI_RoleCode codeListValue="publisher" codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#CI_RoleCode"/>
			</gmd:role>
		</gmd:CI_ResponsibleParty>
	</gmd:contact>
	<gmd:dateStamp>
		<gco:DateTime>'''+now+'''</gco:DateTime>
	</gmd:dateStamp>
	<gmd:metadataStandardName>
		<gco:CharacterString>ISO 19115:2003/19139</gco:CharacterString>
	</gmd:metadataStandardName>
	<gmd:metadataStandardVersion>
		<gco:CharacterString>1.0</gco:CharacterString>
	</gmd:metadataStandardVersion>
	<gmd:spatialRepresentationInfo>
		<gmd:MD_GridSpatialRepresentation>
			<gmd:numberOfDimensions>
				<gco:Integer>'''+str(len(ncdims))+'''</gco:Integer>
			</gmd:numberOfDimensions>
'''+timedim+'''
'''+latdim+'''
'''+londim+'''
'''+levdim+'''
			<gmd:cellGeometry>
				<gmd:MD_CellGeometryCode codeListValue="area" codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#MD_CellGeometryCode"/>
			</gmd:cellGeometry>
			<gmd:transformationParameterAvailability>
				<gco:Boolean>true</gco:Boolean>
			</gmd:transformationParameterAvailability>
		</gmd:MD_GridSpatialRepresentation>
	</gmd:spatialRepresentationInfo>
	<gmd:referenceSystemInfo>
		<gmd:MD_ReferenceSystem>
			<gmd:referenceSystemIdentifier>
				<gmd:RS_Identifier>
					<gmd:code gco:nilReason="missing">
					        <gco:CharacterString/>
					</gmd:code>
				</gmd:RS_Identifier>
			</gmd:referenceSystemIdentifier>
		</gmd:MD_ReferenceSystem>
	</gmd:referenceSystemInfo>
	<gmd:identificationInfo>
		<gmd:MD_DataIdentification>
			<gmd:citation>
				<gmd:CI_Citation>
					<gmd:title>
						<gco:CharacterString>'''+str(getattr(f,'title'))+''' - '''+realfile.split('/')[-1][:-3]+'''</gco:CharacterString>
					</gmd:title>
					<gmd:date>
						<gmd:CI_Date>
							<gmd:date>
								<gco:DateTime>'''+creationDate+'''</gco:DateTime>
							</gmd:date>
							<gmd:dateType>
								<gmd:CI_DateTypeCode codeListValue="publication" codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#CI_DateTypeCode"/>
							</gmd:dateType>
						</gmd:CI_Date>
					</gmd:date>
					<gmd:edition>
						<gco:CharacterString>'''+os.readlink(file1[0])[-8:]+'''</gco:CharacterString>
					</gmd:edition>
				</gmd:CI_Citation>
			</gmd:citation>
			<gmd:purpose>
				<gco:CharacterString>'''+str(getattr(f,'project_id'))+''' '''+model+''' '''+expt+''' '''+freq+''' '''+realm+''' '''+rip+''' '''+dates+''' '''+var+''' '''+varlong+'''</gco:CharacterString>
			</gmd:purpose>
			<gmd:graphicOverview>
				<gmd:MD_BrowseGraphic>
					<gmd:fileName>
						<gco:CharacterString>'''+file1[0]+'''</gco:CharacterString>
					</gmd:fileName>
				</gmd:MD_BrowseGraphic>
			</gmd:graphicOverview>
			<gmd:descriptiveKeywords>
				<gmd:MD_Keywords>
					<gmd:keyword>
						<gco:CharacterString>'''+model+'''</gco:CharacterString>
					</gmd:keyword>
					<gmd:keyword>
						<gco:CharacterString>'''+expt+'''</gco:CharacterString>
					</gmd:keyword>
					<gmd:keyword>
						<gco:CharacterString>'''+freq+'''</gco:CharacterString>
					</gmd:keyword>
					<gmd:keyword>
						<gco:CharacterString>'''+realm+'''</gco:CharacterString>
					</gmd:keyword>
					<gmd:keyword>
						<gco:CharacterString>'''+rip+'''</gco:CharacterString>
					</gmd:keyword>
					<gmd:keyword>
						<gco:CharacterString>'''+var+'''</gco:CharacterString>
					</gmd:keyword>
                                        <gmd:keyword>
						<gco:CharacterString>'''+varlong+'''</gco:CharacterString>
					</gmd:keyword>
					<gmd:keyword>
						<gco:CharacterString>'''+dates+'''</gco:CharacterString>
					</gmd:keyword>
					<gmd:keyword>
					<gco:CharacterString>'''+str(getattr(f,'project_id'))+'''</gco:CharacterString>
					</gmd:keyword>
                                        <gmd:keyword>
					<gco:CharacterString>Climate model data</gco:CharacterString>
					</gmd:keyword>
					<gmd:type>
						<gmd:MD_KeywordTypeCode codeListValue="theme" codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#MD_KeywordTypeCode"/>
					</gmd:type>
				</gmd:MD_Keywords>
			</gmd:descriptiveKeywords>
			<gmd:descriptiveKeywords>
				<gmd:MD_Keywords>
					<gmd:keyword>
						<gco:CharacterString>World</gco:CharacterString>
					</gmd:keyword>
					<gmd:type>
						<gmd:MD_KeywordTypeCode codeListValue="place" codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#MD_KeywordTypeCode"/>
					</gmd:type>
				</gmd:MD_Keywords>
			</gmd:descriptiveKeywords>
			<gmd:abstract>
				<gco:CharacterString>netcdf '''+str(getattr(f,'title'))+''' - '''+realfile.split('/')[-1][:-3]+''' '''+abstract+'''</gco:CharacterString>
			</gmd:abstract>
			<gmd:status>
				<gmd:MD_ProgressCode codeListValue="onGoing" codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#MD_ProgressCode"/>
			</gmd:status>
			<gmd:pointOfContact>
				<gmd:CI_ResponsibleParty>
					<gmd:individualName gco:nilReason="missing">
						<gco:CharacterString/>
					</gmd:individualName>
					<gmd:organisationName>
						<gco:CharacterString>NCI</gco:CharacterString>
					</gmd:organisationName>
					<gmd:positionName gco:nilReason="missing">
						<gco:CharacterString/>
					</gmd:positionName>
					<gmd:contactInfo>
						<gmd:CI_Contact>
							<gmd:phone>
								<gmd:CI_Telephone>
									<gmd:voice gco:nilReason="missing">
										<gco:CharacterString/>
									</gmd:voice>
									<gmd:facsimile gco:nilReason="missing">
										<gco:CharacterString/>
									</gmd:facsimile>
								</gmd:CI_Telephone>
							</gmd:phone>
							<gmd:address>
								<gmd:CI_Address>
									<gmd:deliveryPoint gco:nilReason="missing">
										<gco:CharacterString/>
									</gmd:deliveryPoint>
									<gmd:city gco:nilReason="missing">
										<gco:CharacterString/>
									</gmd:city>
									<gmd:administrativeArea gco:nilReason="missing">
										<gco:CharacterString/>
									</gmd:administrativeArea>
									<gmd:postalCode gco:nilReason="missing">
										<gco:CharacterString/>
									</gmd:postalCode>
									<gmd:country>
										<gco:CharacterString>Australia</gco:CharacterString>
									</gmd:country>
									<gmd:electronicMailAddress>
										<gco:CharacterString>esg_publishing@nf.nci.org.au</gco:CharacterString>
									</gmd:electronicMailAddress>
								</gmd:CI_Address>
							</gmd:address>
						</gmd:CI_Contact>
					</gmd:contactInfo>
					<gmd:role>
						<gmd:CI_RoleCode codeListValue="publisher" codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#CI_RoleCode"/>
					</gmd:role>
				</gmd:CI_ResponsibleParty>
			</gmd:pointOfContact>
			<gmd:resourceMaintenance>
				<gmd:MD_MaintenanceInformation>
					<gmd:maintenanceAndUpdateFrequency>
						<gmd:MD_MaintenanceFrequencyCode codeListValue="asNeeded" codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#MD_MaintenanceFrequencyCode"/>
					</gmd:maintenanceAndUpdateFrequency>
				</gmd:MD_MaintenanceInformation>
			</gmd:resourceMaintenance>
			<gmd:graphicOverview>
				<gmd:MD_BrowseGraphic>
					<gmd:fileName gco:nilReason="missing">
						<gco:CharacterString/>
					</gmd:fileName>
					<gmd:fileDescription>
						<gco:CharacterString>thumbnail</gco:CharacterString>
					</gmd:fileDescription>
				</gmd:MD_BrowseGraphic>
			</gmd:graphicOverview>
			<gmd:graphicOverview>
				<gmd:MD_BrowseGraphic>
					<gmd:fileName gco:nilReason="missing">
						<gco:CharacterString/>
					</gmd:fileName>
					<gmd:fileDescription>
						<gco:CharacterString>large_thumbnail</gco:CharacterString>
					</gmd:fileDescription>
				</gmd:MD_BrowseGraphic>
			</gmd:graphicOverview>
			<gmd:resourceConstraints>
				<gmd:MD_LegalConstraints>
					<gmd:accessConstraints>
						<gmd:MD_RestrictionCode codeListValue="license" codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#MD_RestrictionCode"/>
					</gmd:accessConstraints>
					<gmd:useConstraints>
						<gmd:MD_RestrictionCode codeListValue="license" codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#MD_RestrictionCode"/>
					</gmd:useConstraints>
					<gmd:otherConstraints>
						<gco:CharacterString>http://cmip-pcmdi.llnl.gov/cmip5/terms.html</gco:CharacterString>
					</gmd:otherConstraints>
				</gmd:MD_LegalConstraints>
			</gmd:resourceConstraints>
                        <gmd:metadataConstraints>
                                <gmd:MD_SecurityConstraints>
                                        <gmd:classification>
                                                <gmd:MD_ClassificationCode codeListValue="unclassified" codeList="http://www.ngdc.noaa.gov/metadata/published/xsd/schema/resources/Codelist/gmxCodelists.xml#MD_ClassificationCode"/>
                                        </gmd:classification>
                                </gmd:MD_SecurityConstraints>
                        </gmd:metadataConstraints>
			<gmd:spatialRepresentationType>
				<gmd:MD_SpatialRepresentationTypeCode codeListValue="'''+gridvec+'''" codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#MD_SpatialRepresentationTypeCode"/>
			</gmd:spatialRepresentationType>
			<gmd:language>
				<gco:CharacterString>eng</gco:CharacterString>
			</gmd:language>
			<gmd:characterSet>
				<gmd:MD_CharacterSetCode codeListValue="utf8" codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#MD_CharacterSetCode"/>
			</gmd:characterSet>
			<gmd:topicCategory>
				<gmd:MD_TopicCategoryCode>boundaries</gmd:MD_TopicCategoryCode>
			</gmd:topicCategory>
'''+timeextent+'''
			<gmd:extent>
				<gmd:EX_Extent>
					<gmd:geographicElement>
						<gmd:EX_GeographicBoundingBox>
							<gmd:westBoundLongitude>
								<gco:Decimal>'''+Wbound+'''</gco:Decimal>
							</gmd:westBoundLongitude>
							<gmd:eastBoundLongitude>
								<gco:Decimal>'''+Ebound+'''</gco:Decimal>
							</gmd:eastBoundLongitude>
							<gmd:southBoundLatitude>
								<gco:Decimal>'''+Sbound+'''</gco:Decimal>
							</gmd:southBoundLatitude>
							<gmd:northBoundLatitude>
								<gco:Decimal>'''+Nbound+'''</gco:Decimal>
							</gmd:northBoundLatitude>
						</gmd:EX_GeographicBoundingBox>
					</gmd:geographicElement>
				</gmd:EX_Extent>
			</gmd:extent>
			<gmd:supplementalInformation gco:nilReason="missing">
				<gco:CharacterString/>
			</gmd:supplementalInformation>
		</gmd:MD_DataIdentification>
	</gmd:identificationInfo>
	<gmd:distributionInfo>
		<gmd:MD_Distribution>
			<gmd:transferOptions>
				<gmd:MD_DigitalTransferOptions>
					<!--gmd:onLine>
						<gmd:CI_OnlineResource>
							<gmd:linkage>
								<gmd:URL>http://localhost:8080'''+file1[0]+'''</gmd:URL>
							</gmd:linkage>
							<gmd:protocol>
								<gco:CharacterString>FILE</gco:CharacterString>
							</gmd:protocol>
							<gmd:name>
								<gco:CharacterString>'''+realfile.split('/')[-1]+'''</gco:CharacterString>
							</gmd:name>
							<gmd:description>
								<gco:CharacterString>NetCDF data file at NCI</gco:CharacterString>
							</gmd:description>
						</gmd:CI_OnlineResource>
					</gmd:onLine-->
					<gmd:onLine>
                                                <gmd:CI_OnlineResource>
							<gmd:linkage>
								<gmd:URL>'''+file1[0]+'''</gmd:URL>
							</gmd:linkage>
							<gmd:protocol>
								<gco:CharacterString>FILE</gco:CharacterString>
							</gmd:protocol>
							<gmd:name>
								<gco:CharacterString>'''+realfile.split('/')[-1]+'''</gco:CharacterString>
							</gmd:name>
							<gmd:description>
								<gco:CharacterString>NetCDF data file at NCI: '''+file1[0]+'''</gco:CharacterString>
							</gmd:description>
						</gmd:CI_OnlineResource>
					</gmd:onLine>
					<gmd:onLine>
						<gmd:CI_OnlineResource>
							<gmd:linkage>
								<gmd:URL>http://dapds00.nci.org.au/thredds/fileServer/CMIP5/derived/CMIP5/GCM/native/'''+'/'.join(file1[0].split('/')[7:12])+'''/'''+file1[0].split('_')[1]+'''/'''+file1[0].split('/')[13]+'''/latest/'''+file1[0].split('/')[12]+'''/'''+realfile.split('/')[-1]+'''</gmd:URL>
							</gmd:linkage>
							<gmd:protocol>
								<gco:CharacterString>FILE</gco:CharacterString>
							</gmd:protocol>
							<gmd:name>
								<gco:CharacterString>'''+realfile.split('/')[-1][:-3]+'''-seasavg_native.nc</gco:CharacterString>
							</gmd:name>
							<gmd:description>
								<gco:CharacterString>NCI OPeNDAP download data</gco:CharacterString>
							</gmd:description>
						</gmd:CI_OnlineResource>
					</gmd:onLine>
					<!--gmd:onLine>
						<gmd:CI_OnlineResource>
							<gmd:linkage>
								<gmd:URL>http://localhost:8123/geonetwork/srv/en/metadata.show?uuid=4294e6ae-9c7c-462f-a7c5-6cbe0a7c8b90</gmd:URL>
							</gmd:linkage>
							<gmd:protocol>
								<gco:CharacterString>WWW:LINK-1.0-http-related</gco:CharacterString>
							</gmd:protocol>
							<gmd:name gco:nilReason="missing">
								<gco:CharacterString/>
							</gmd:name>
						</gmd:CI_OnlineResource>
					</gmd:onLine-->
				</gmd:MD_DigitalTransferOptions>
			</gmd:transferOptions>
		</gmd:MD_Distribution>
	</gmd:distributionInfo>
	<gmd:dataQualityInfo>
		<gmd:DQ_DataQuality>
			<gmd:scope>
				<gmd:DQ_Scope>
					<gmd:level>
						<gmd:MD_ScopeCode codeListValue="dataset" codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#MD_ScopeCode"/>
					</gmd:level>
				</gmd:DQ_Scope>
			</gmd:scope>
			<gmd:lineage>
				<gmd:LI_Lineage>
					<gmd:statement>
						<gco:CharacterString>'''+lineage+'''.</gco:CharacterString>
					</gmd:statement>
				</gmd:LI_Lineage>
			</gmd:lineage>
		</gmd:DQ_DataQuality>
	</gmd:dataQualityInfo>
</gmd:MD_Metadata>
''')

    wrfile.close()
else:
    print "File already exists"
