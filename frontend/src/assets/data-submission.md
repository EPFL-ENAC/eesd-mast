### Instructions

To report a new building experiment, there are some data format conventions to follow.

#### Reference Publication

The building experiment was reported in a reference publication.

If the reference publication is already declared in the database, use its reference ID in the building experiment description.

If the reference publication is not in the database, you will provide the following information:

- **Reference**: short reference publication identifier (must be unique), ex. "Beyer et al. (2015)"
- **Full Reference**: long reference publication with authors, title, editor etc.
- **Link To Experimental Paper**: permanent link to the publication, ex. "https://doi.org/10.1007/s10518-015-9752-z"
- **Publication Year**
- **Corresponding Author Name**
- **Corresponding Author Email**
- **Request Data Available**: one of "Openly available", "Not available" or "Available on request"
- **Link To Request Data**: a web link to a data access request site (optional)

#### Building Experiment

The description of a building experiment will provide the following information:

- **Description**
- **Test Scale**
- **Simultaneous Excitations Nb**
- **Applied Excitation Directions**
- **Storeys Nb**
- **Building Height**
- **Total Building Height**
- **Diaphragm Material**
- **Roof Material Geometry**
- **Masonry Unit Type**
- **Masonry Unit Material**
- **Mortar Type**
- **Masonry Compressive Strength**
- **Masonry Wall Thickness**
- **Wall Leaves Nb**
- **Internal Walls**
- **Mechanical Connectors**
- **Connectors Activation**
- **Retrofitted**
- **Retrofitting Application**
- **Retrofitting Type**
- **First Estimated Fundamental Period**
- **Last Estimated Fundamental Period**
- **Max Horizontal PGA**
- **Max Estimated DG**
- **Material Characterizations**
- **Associated Test Types**
- **Material Characterization References**
- **Digitalized Data**
- **Experimental Results Reported**
- **Open Measured Data**
- **Link To Open Measured Data**
- **Crack Types Observed**
- **Experimental Campaign Motivation**
- **Publication Year**
- **Reference ID**

##### Test Results

- **Run ID**
- **Nominal PGA X**
- **Nominal PGA Y**
- **Nominal PGA Z**
- **Actual PGA X**
- **Actual PGA Y**
- **Actual PGA Z**
- **DG Reported**
- **DG Derived**
- **Max Top Drift X**
- **Max Top Drift Y**
- **Residual Top Drift X**
- **Residual Top Drift Y**
- **Base Shear Coef**
- **Reported T1 X**
- **Reported T1 Y**
- **Experiment ID**

##### Files

The experiment's file repository layout conventions are:

```
.
├── README.md
│
├── LICENSE.md
│
├── 3D model
│   └── main.vtk (or main.vtp)
│
├── Crack maps
│   ├── <Run ID>.png
│   └── ...
│
├── Global force-displacement curve
│   ├── <Run ID>.txt
│   └── ...
│
├── Shake-table accelerations
│   ├── <Run ID>.txt
│   └── ...
│
└── Top displacement histories
    ├── <Run ID>.txt
    └── ...
```

where:

- _README_ and _LICENSE_ files are optional but highly recommended,
- The 3D model can be in multiple files in VTK format (both `.vtk` or `.vtp` file extensions are supported),
- `Run ID` is one of the run results identifiers declared in the database,
- `.md` files are in [Markdown format](https://commonmark.org/),
- `.png` files are images,
- `.txt` files are data files in tab separated values format.

### Command Line Tool

A command line tool is available for querying the database, extracting building experiment files, preparing data to upload and more. See usage instructions of [MAST CLI](https://github.com/EPFL-ENAC/eesd-mast-cli)
