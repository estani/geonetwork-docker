#HOWTO

####Begin

* Build the local docker containers of our nodes

			% ./search/build
	 		% ./publisher/build/

* Start up some elastic __search__ nodes
	
	Search containers run as long lived daemon containers.
	
		% search/run -n test1
		% search/run -n test2
		% search/run -n test3
		% search/run -n test4
		% search/run -n test5
		% search/run -n test6
		
		% docker ps
Verify that the nodes (in containers) are running....

	<pre>
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS                           NAMES
196b9c1870cc        search:latest       "/container/boot"   54 seconds ago      Up 54 seconds       10101/tcp, 9200/tcp, 9300/tcp   test7
3dbc0bffc503        search:latest       "/container/boot"   18 minutes ago      Up 18 minutes       10101/tcp, 9200/tcp, 9300/tcp   test6
0d829d5d0bb3        search:latest       "/container/boot"   18 minutes ago      Up 18 minutes       10101/tcp, 9200/tcp, 9300/tcp   test5
f68e2897741b        search:latest       "/container/boot"   18 minutes ago      Up 18 minutes       9300/tcp, 10101/tcp, 9200/tcp   test4
7aa32d283e7b        search:latest       "/container/boot"   23 minutes ago      Up 23 minutes       9300/tcp, 10101/tcp, 9200/tcp   test3
f448e9aee233        search:latest       "/container/boot"   About an hour ago   Up About an hour    9300/tcp, 10101/tcp, 9200/tcp   test2
c6cac5a5b008        search:latest       "/container/boot"   About an hour ago   Up About an hour    9200/tcp, 9300/tcp, 10101/tcp   test1
</pre>		
	
* Engage up the __publisher__

	Note: publisher containers live only for as long as the publication process.  They do not run as long lived processes like search (index) nodes.
	
	Let's just take a look at the JSON that will be harvested from the netcdf file(s) [no publishing to the index yet].  We make use of the --dry-run and --show flags.
	
		% publisher/bin/nc2json --include '.*nc$' --show --dir-structure /*/*/model2  publisher/claire_src/thetao_Omon_ACCESS1-0_historical_r1i1p1_200001-200412.nc
		
	The output should be the JSON representation fo the full netCDF metadata:

	<pre>
{
  "original_path": "/workbench/publisher/claire_src/thetao_Omon_ACCESS1-0_historical_r1i1p1_200001-200412.nc",
  "model2": "claire_src",
  "variables": {
    "time_bnds": {
      "dimensions": [
        "time",
        "bnds"
      ]
    },
    "lon_vertices": {
      "units": "degrees_east",
      "dimensions": [
        "j",
        "i",
        "vertices"
      ]
    },
    "i": {
      "units": "1",
      "long_name": "cell index along first dimension",
      "dimensions": [
        "i"
      ]
    },
    "j": {
      "units": "1",
      "long_name": "cell index along second dimension",
      "dimensions": [
        "j"
      ]
    },
    "lon": {
      "units": "degrees_east",
      "long_name": "longitude coordinate",
      "standard_name": "longitude",
      "dimensions": [
        "j",
        "i"
      ],
      "bounds": "lon_vertices"
    },
    "lev_bnds": {
      "dimensions": [
        "lev",
        "bnds"
      ]
    },
    "lev": {
      "dimensions": [
        "lev"
      ],
      "positive": "down",
      "bounds": "lev_bnds",
      "long_name": "ocean depth coordinate",
      "standard_name": "depth",
      "units": "m",
      "axis": "Z"
    },
    "time": {
      "dimensions": [
        "time"
      ],
      "bounds": "time_bnds",
      "long_name": "time",
      "standard_name": "time",
      "units": "days since 0001-01-01",
      "calendar": "proleptic_gregorian",
      "axis": "T"
    },
    "lat": {
      "units": "degrees_north",
      "long_name": "latitude coordinate",
      "standard_name": "latitude",
      "dimensions": [
        "j",
        "i"
      ],
      "bounds": "lat_vertices"
    },
    "lat_vertices": {
      "units": "degrees_north",
      "dimensions": [
        "j",
        "i",
        "vertices"
      ]
    },
    "thetao": {
      "_FillValue": "1e+20",
      "dimensions": [
        "time",
        "lev",
        "j",
        "i"
      ],
      "associated_files": "baseURL: http://cmip-pcmdi.llnl.gov/CMIP5/dataLocation gridspecFile: gridspec_ocean_fx_ACCESS1-0_historical_r0i0p0.nc areacello: areacello_fx_ACCESS1-0_historical_r0i0p0.nc volcello: volcello_fx_ACCESS1-0_historical_r0i0p0.nc",
      "coordinates": "lat lon",
      "long_name": "Sea Water Potential Temperature",
      "standard_name": "sea_water_potential_temperature",
      "original_units": "deg_C",
      "cell_measures": "area: areacello volume: volcello",
      "cell_methods": "time: mean",
      "units": "K",
      "missing_value": "1e+20",
      "history": "2012-01-15T21:17:54Z altered by CMOR: Converted units from 'deg_C' to 'K'. 2012-01-15T21:17:54Z altered by CMOR: replaced missing value flag (-1e+20) with standard missing value (1e+20)."
    }
  },
  "global": {
    "initialization_method": "1",
    "product": "output",
    "creation_date": "2012-01-15T21:17:56Z",
    "frequency": "mon",
    "references": "See http://wiki.csiro.au/confluence/display/ACCESS/ACCESS+Publications",
    "title": "ACCESS1-0 model output prepared for CMIP5 historical",
    "source": "ACCESS1-0 2011. Atmosphere: AGCM v1.0 (N96 grid-point, 1.875 degrees EW x approx 1.25 degree NS, 38 levels); ocean: NOAA/GFDL MOM4p1 (nominal 1.0 degree EW x 1.0 degrees NS, tripolar north of 65N, equatorial refinement to 1/3 degree from 10S to 10 N, cosine dependent NS south of 25S, 50 levels); sea ice: CICE4.1 (nominal 1.0 degree EW x 1.0 degrees NS, tripolar north of 65N, equatorial refinement to 1/3 degree from 10S to 10 N, cosine dependent NS south of 25S); land: MOSES2 (1.875 degree EW x 1.25 degree NS, 4 levels",
    "experiment": "historical",
    "realization": "1",
    "project_id": "CMIP5",
    "institute_id": "CSIRO-BOM",
    "model_id": "ACCESS1-0",
    "parent_experiment_id": "piControl",
    "experiment_id": "historical",
    "cmor_version": "2.8.0",
    "parent_experiment": "pre-industrial control",
    "modeling_realm": "ocean",
    "branch_time": 109207.0,
    "institution": "CSIRO (Commonwealth Scientific and Industrial Research Organisation, Australia), and BOM (Bureau of Meteorology, Australia)",
    "version_number": "v20120115",
    "forcing": "GHG, Oz, SA, Sl, Vl, BC, OC, (GHG = CO2, N2O, CH4, CFC11, CFC12, CFC113, HCFC22, HFC125, HFC134a)",
    "physics_version": "1",
    "Conventions": "CF-1.4",
    "contact": "The ACCESS wiki: http://wiki.csiro.au/confluence/display/ACCESS/Home. Contact Tony.Hirst@csiro.au regarding the ACCESS coupled climate model. Contact Peter.Uhe@csiro.au regarding ACCESS coupled climate model CMIP5 datasets.",
    "table_id": "Table Omon (27 April 2011) 694b38a3f68f18e58ba80230aa4746ea",
    "tracking_id": "3862bfe1-9ac6-4de9-a7bd-8c36ae9697f5",
    "parent_experiment_rip": "r1i1p1",
    "history": "CMIP5 compliant file produced from raw ACCESS model output using the ACCESS Post-Processor and CMOR2. 2012-01-15T21:17:56Z CMOR rewrote data to comply with CF standards and CMIP5 requirements."
  },
  "dimensions": {
    "bnds": {
      "unlimited": false,
      "size": 2
    },
    "i": {
      "unlimited": false,
      "size": 360
    },
    "j": {
      "unlimited": false,
      "size": 300
    },
    "vertices": {
      "unlimited": false,
      "size": 4
    },
    "lev": {
      "unlimited": false,
      "size": 50
    },
    "time": {
      "unlimited": true,
      "size": 60
    }
  }
}
</pre>
	
	To perform the actual publication operation and post this JSON into the elastic search index, do the following:
	
		publisher/bin/nc2es -n test6 --include '.*nc$' --dir-structure /*/model publisher/claire_src/thetao_Omon_ACCESS1-0_historical_r1i1p1_200001-200412.nc
		
	To check that the data has been indexed, there is a quick handy query script that you can use to do some basic sanity checking
	
		publisher/bin/query -n test6 -q '*:*' | grep original_path
	Results in...
	
		"original_path": "/workbench/publisher/claire_src/thetao_Omon_ACCESS1-0_historical_r1i1p1_200001-200412.nc",
		
	One thing to notice is the --dir-structure /*/model and the actual directory structure that is used when publishing /workbench/publisher/claire_src.  It will use the second token in the absolute path as the value for "model" in the metadata.
	