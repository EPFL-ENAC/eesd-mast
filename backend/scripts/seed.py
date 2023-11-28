"""
CLI for uploading Excel to database
"""
from argparse import ArgumentParser
from logging import DEBUG, INFO, basicConfig, debug

import pandas as pd
from math import isnan
from numbers import Number
import re
import numpy as np

from mast.database import engine

def main():
    parser = ArgumentParser(description="Upload Excel file to database")
    parser.add_argument("filename", help="data input file pattern")

    args = parser.parse_args()
    filename: str = args.filename

    debug(f"connecting to {engine.url}")
    debug(f"seeding with {filename}")

    Database_summary = pd.read_excel(open(filename, "rb"), sheet_name="Summary")

    # Initialize an empty list to store the data
    data_summary = []

    # Iterate through the rows
    for index, row in Database_summary.iterrows():
        # Check if the row is empty (all NaN values)
        if row.isnull().all():
            break  # Exit the loop if an empty row is encountered
        data_summary.append(row)
        
    # Convert the collected data to a new DataFrame
    experiment = pd.DataFrame(data_summary)

    # Rename the columns
    experiment.rename(columns = {
        "Building #": "id",
        "Scheme": "scheme",
        "Reference": "reference",
        "Publication year": "publication_year",
        "Short description": "description",
        "Experiment ID": "experiment_id",
        "Scale of test": "test_scale",
        "Number of simultaneous excitations": "simultaneous_excitations_nb",
        "Directions of applied excitations": "applied_excitation_directions",
        "Number of test runs": "run_results_nb",
        "Number of storeys": "storeys_nb",
        "Total building height": "total_building_height",
        "Diaphragm material": "diaphragm_material",
        "Roof material and geometry": "roof_material_geometry",
        "Type of masonry unit": "masonry_unit_type",
        "Masonry unit material": "masonry_unit_material",
        "Mortar type": "mortar_type",
        "Compressive strength of masonry": "masonry_compressive_strength",
        "Masonry walls thickness": "masonry_wall_thickness",
        "Number of wall leaves": "wall_leaves_nb",
        "Internal walls": "internal_walls",
        "Mechanical connectors present": "mechanical_connectors",
        "Activation of connectors": "connectors_activation",
        "Retrofitted": "retrofitted",
        "Application of retrofitting": "retrofitting_application",
        "Type of retrofitting": "retrofitting_type",
        "First estimated fundamental period": "first_estimated_fundamental_period",
        "Last estimated fundamental period": "last_estimated_fundamental_period",
        "Maximum horizontal PGA": "max_horizontal_pga",
        "Maximum estimated DG": "max_estimated_dg",
        "Material characterization available": "material_characterizations",
        "Associated type of test": "associated_test_types",
        "Reference for material characterization": "material_characterization_refs",
        "Experimental results reported": "experimental_results_reported",
        "Measured data openly available as digital files": "open_measured_data",
        "Link to request data": "link_to_request_data",
        "Digitalized data available": "digitalized_data",
        "Types of cracks observed": "crack_types_observed",
        "Motivation of the experimental campaign": "experimental_campaign_motivation",
        "Link to experimental paper": "link_to_experimental_paper",
        "Corresponding author": "corresponding_author_name",
    }, inplace=True)
    
    # Drop some columns
    del experiment["id"]
    del experiment["scheme"] # do not handle scheme image yet

    # Split author string
    experiment[["corresponding_author_name", "corresponding_author_email"]] = experiment["corresponding_author_name"].str.rsplit("\n", n=1, expand=True)
    
    # Prepare array values
    def array_formatter(x):
        if isinstance(x, Number) and isnan(x):
            return None
        if isinstance(x, str):
            x = x.strip()
            x = "\",\"".join(re.split(r"\n|/", x))
        return f"{{\"{x}\"}}"
    for col in ["applied_excitation_directions", "masonry_wall_thickness", "retrofitting_type", "material_characterizations", "material_characterization_refs", "associated_test_types", "experimental_results_reported", "crack_types_observed"]:
        experiment[col] = experiment[col].apply(array_formatter)

    # Clean number values
    def number_cleanup(x):
        if not isinstance(x, Number):
            return None
        return x
    for col in ["publication_year", "run_results_nb", "storeys_nb", "total_building_height", "masonry_compressive_strength", "wall_leaves_nb", "first_estimated_fundamental_period", "last_estimated_fundamental_period", "max_horizontal_pga", "max_estimated_dg"]:
        experiment[col] = experiment[col].apply(number_cleanup)

    # Split open measures data field
    experiment["link_to_open_measured_data"] = experiment["open_measured_data"].map(lambda x: x if x.startswith("http") else None)
    
    # Clean boolean values
    def yesno_cleanup(x):
        return x != None and x != "No"
    for col in ["open_measured_data", "digitalized_data", "internal_walls", "retrofitted"]:
        experiment[col] = experiment[col].apply(yesno_cleanup)

    # References    
    reference = experiment[["reference", "publication_year", "link_to_experimental_paper", "corresponding_author_name", "corresponding_author_email", "link_to_request_data"]].drop_duplicates().copy()
    reference["request_data_available"] = reference["link_to_request_data"].map(lambda x: x if not x.startswith("http") else "Available on request")
    reference["link_to_request_data"] = reference["link_to_request_data"].map(lambda x: x if x.startswith("http") else None)
    reference.index = np.arange(1, len(reference)+1)

    # Experiments
    experiment["reference_id"] = experiment["reference"].map(lambda x: reference[reference["reference"] == x].index[0])
    experiment = experiment.drop(["reference", "publication_year", "link_to_experimental_paper", "corresponding_author_name", "corresponding_author_email", "link_to_request_data"], axis=1)
    experiment.index = np.arange(1, len(experiment)+1)

    # Full references
    Database_references = pd.read_excel(open(filename, "rb"), sheet_name="References", usecols="A:C", header=1)
    Database_references.drop("Excel sheet name", axis=1, inplace=True)
    Database_references.rename(columns={"Building #": "experiment_id", "Reference": "full_reference"}, inplace=True)
    full_reference = pd.merge(experiment[["reference_id"]], Database_references, left_index=True, right_on="experiment_id").drop("experiment_id", axis=1).drop_duplicates()
    reference = pd.merge(reference, full_reference, left_index=True, right_on="reference_id").drop("reference_id", axis=1)

    # Write the DataFrame to the database
    debug(f"writing references to {engine.url}")
    reference.to_sql("reference", engine, if_exists="append", index=False)

    # Write the DataFrame to the database
    debug(f"writing experiments to {engine.url}")
    experiment.to_sql("experiment", engine, if_exists="append", index=False)

    # Run results
    def run_id_check(x):
        if isinstance(x, Number):
            return not isnan(x)
        return x != None and x.strip() != "-" and x.strip() != "Initial" and x.strip() != "Final"

    for i in range(1, len(experiment)+1):
        debug(f"reading sheet (B{i})")
        results = pd.read_excel(open(filename, "rb"), sheet_name=f"B{i}", usecols="F:U", header=2)
        results = results.loc[results["Run ID"].apply(run_id_check)]
        results.rename(columns = {
            "Run ID": "run_id",
            "Nominal PGA X": "nominal_pga_x",
            "Nominal PGA Y": "nominal_pga_y",
            "Nominal PGA Z": "nominal_pga_z",
            "Actual PGA X": "actual_pga_x",
            "Actual PGA Y": "actual_pga_y",
            "Actual PGA Z": "actual_pga_z",
            "DG reported": "dg_reported",
            "DG derived": "dg_derived",
            "Max. Top Drift X": "max_top_drift_x",
            "Max. Top Drift Y": "max_top_drift_y",
            "Res. Top Drift X": "residual_top_drift_x",
            "Res. Top Drift Y": "residual_top_drift_y",
            "Base shear coef.": "base_shear_coef",
            "Reported T1X": "reported_t1_x",
            "Reported T1Y": "reported_t1_y",
        }, inplace=True)
        results["experiment_id"] = np.repeat(i, len(results))
        debug(f"writing run results from experiment B{i} to {engine.url}")
        results.to_sql("run_result", engine, if_exists="append", index=False)


if __name__ == "__main__":
    basicConfig(level=DEBUG)
    main()