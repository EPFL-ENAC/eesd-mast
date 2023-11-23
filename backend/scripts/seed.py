"""
CLI for uploading Excel to database
"""
from argparse import ArgumentParser
from logging import DEBUG, INFO, basicConfig, debug

import pandas as pd
from mast.database import engine

def main():
    parser = ArgumentParser(description="Upload Excel file to database")
    parser.add_argument("filename", help="data input file pattern")

    args = parser.parse_args()
    filename: str = args.filename

    debug(f"connecting to {engine.url}")
    debug(f"seeding with {filename}")

    Database_summary = pd.read_excel(open(filename, 'rb'), sheet_name='Summary')

    # Initialize an empty list to store the data
    data_summary = []

    # Iterate through the rows
    for index, row in Database_summary.iterrows():
        # Check if the row is empty (all NaN values)
        if row.isnull().all():
            break  # Exit the loop if an empty row is encountered
        data_summary.append(row)
        
    # Convert the collected data to a new DataFrame
    test_summary = pd.DataFrame(data_summary)

    # Rename the columns
    debug(f"test_summary.columns: {test_summary.columns}")
    test_summary.columns = [
        "id",                                 # 'Building ID'
        "scheme",                             # 'Scheme'
        "reference",                          # 'Reference',
        "publication_year",                   # 'Publication year'
        "description",                        # 'Short description'
        "experiment_id",                      # 'Experiment ID'
        "test_scale",                         # 'Scale of test'
        "simultaneous_excitations_nb",        # 'Number of simultaneous excitations'
        "applied_excitations_direction",      # 'Directions of applied excitations'
        "test_runs_nb",                       # 'Number of test runs'
        "storeys_nb",                         # 'Number of storeys'
        "total_building_height",              # 'Total building height'
        "diaphragm_material",                 # 'Diaphragm material'
        "roof_material_geometry",             # 'Roof material and geometry'
        "masonry_unit_type",                  # 'Type of masonry unit'
        "masonry_unit_material",              # 'Masonry unit material'
        "mortar_type",                        # 'Mortar type'
        "masonry_compressive_strength",       # 'Compressive strength of masonry'
        "masonry_wall_thickness",             # 'Masonry walls thickness'
        "wall_leaves_nb",                     # 'Number of wall leaves'
        "internal_walls",                     # 'Internal walls'
        "mechanical_connectors",              # 'Mechanical connectors present'
        "connectors_activation",              # 'Activation of connectors'
        "retrofitted",                        # 'Retrofitted'
        "retrofitting_application",           # 'Application of retrofitting'
        "retrofitting_type",                  # 'Type of retrofitting'
        "first_estimated_fundamental_period", # 'First estimated fundamental period'
        "last_estimated_fundamental_period",  # 'Last estimated fundamental period'
        "max_horizontal_pga",                 # 'Maximum horizontal PGA'
        "max_estimated_dg",                   # 'Maximum estimated DG'
        "material_characterizations",         # 'Material characterization available'
        "associated_test_types",              # 'Associated type of test'
        "material_characterization_ref",      # 'Reference for material characterization'
        "experimental_results_reported",      # 'Experimental results reported'
        "open_measured_data",                 # 'Measured data openly available as digital files'
        "link_to_request_data",               # 'Link to request data'
        "digitalized_data",                   # 'Digitalized data available'
        "crack_types_observed",               # 'Types of cracks observed'
        "experimental_campaign_motivation",   # 'Motivation of the experimental campaign'
        "link_to_experimental_paper",         # 'Link to experimental paper'
        "corresponding_author_name",          # 'Corresponding author'
    ]

    # Drop some columns
    del test_summary["id"]
    del test_summary["scheme"] # do not handle scheme image yet

    # Split author string
    test_summary[["corresponding_author_name", "corresponding_author_email"]] = test_summary["corresponding_author_name"].str.rsplit("\n", n=1, expand=True)
    
    # Prepare array values
    test_summary["retrofitting_type"] = test_summary.agg("{0[retrofitting_type]}".format, axis=1)

    # Write the DataFrame to the database
    debug(f"writing to {engine.url}")
    test_summary.to_sql("test_summary", engine, if_exists="append", index=False)


if __name__ == "__main__":
    basicConfig(level=DEBUG)
    main()