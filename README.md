# EESD - MAST

MAST (MAsonry Shake-Table) is a comprehensive database and collaborative resource for advancing seismic assessment of unreinforced masonry buildings.

Visit [EESD lab at EPFL](https://www.epfl.ch/labs/eesd/).

## Data provisioning

1. Download the folder from Share point: `Advanced Services > 0145 - MAST Open DB > Data > 00_MAST_database`

2. Setup the [MAST CLI](https://github.com/EPFL-ENAC/eesd-mast-cli) tool. All the write operation require an API key, then get the one from your server deployment.

3. Excel database

  * Upload main dataset from the `Shake_Table_Tests_Database_XXXXX.xlsx` Excel file using `mast upload`. This will populate the experiments, the references and the run result entries in the database.
  * Upload models dataset from the `Modeling assumptions.xlsx` Excel file using `mast upload-models`. This will populate the numerical models entries in the database. Note the "Build IDs" must match.

4. Upload files

  * Upload files in bulk using `mast upload-repo-bulk`. Note the "Build IDs" must match.
  * See `mast help` for more fine grained commands.