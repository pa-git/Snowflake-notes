import os

# Base directory for all output files
BASE_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "extracted_values")

# Ensure the base output directory exists
os.makedirs(BASE_OUTPUT_DIR, exist_ok=True)

# Mapping of cubes to their specific output directories and dimensions
CUBE_CONFIG = {
    "Management Reporting": {
        "output_dir": os.path.join(BASE_OUTPUT_DIR, "management_reporting"),
        "dimensions": ["Account", "Region", "Product"],
    },
    "Sales Analysis": {
        "output_dir": os.path.join(BASE_OUTPUT_DIR, "sales_analysis"),
        "dimensions": ["Customer", "Salesperson", "Product"],
    },
    "Inventory Management": {
        "output_dir": os.path.join(BASE_OUTPUT_DIR, "inventory_management"),
        "dimensions": ["Warehouse", "Product", "Category"],
    },
}

# Ensure all cube-specific output directories exist
for cube in CUBE_CONFIG.values():
    os.makedirs(cube["output_dir"], exist_ok=True)




-------------------

from finpyalpyn.server.config import ServerConfig, Environment, Instance
from TM1py import TM1Service
from data_extraction.utils import process_dimension
from data_extraction.config import CUBE_CONFIG


def extract_data(environment: Environment, instance: Instance, cube_name: str):
    """
    Extract data from a specified cube in TM1 and write dimension data to JSONL files.

    Args:
        environment (Environment): The TM1 environment to connect to.
        instance (Instance): The TM1 instance to use.
        cube_name (str): The name of the cube to extract data from.
    """
    cube_config = CUBE_CONFIG.get(cube_name)

    if not cube_config:
        raise ValueError(f"No configuration found for the cube: {cube_name}")

    dimensions_to_process = cube_config["dimensions"]
    output_dir = cube_config["output_dir"]

    with TM1Service(**ServerConfig.get_config(environment, instance)) as tm1:
        cube = tm1.cubes.get(cube_name)
        cube_dimensions = cube.dimensions

        # Process only the dimensions specified for this cube
        for dimension_name in cube_dimensions:
            if dimension_name in dimensions_to_process:
                output_file = f"{output_dir}/{dimension_name}.jsonl"
                process_dimension(tm1, dimension_name, cube_name, output_file)


if __name__ == "__main__":
    # Example usage
    extract_data(Environment.DEV, Instance.FINANCE, 'Management Reporting')




