import os

# Path to the directory where JSONL files will be saved
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "extracted_values")

# Ensure the output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Mapping of cubes to dimensions to process
CUBE_DIMENSION_MAP = {
    "Management Reporting": ["Account", "Region", "Product"],
    "Sales Analysis": ["Customer", "Salesperson", "Product"],
    "Inventory Management": ["Warehouse", "Product", "Category"],
}


--------------------------

from finpyalpyn.server.config import ServerConfig, Environment, Instance
from TM1py import TM1Service
from data_extraction.utils import process_dimension
from data_extraction.config import OUTPUT_DIR, CUBE_DIMENSION_MAP


def extract_data(environment: Environment, instance: Instance, cube_name: str):
    """
    Extract data from a specified cube in TM1 and write dimension data to JSONL files.

    Args:
        environment (Environment): The TM1 environment to connect to.
        instance (Instance): The TM1 instance to use.
        cube_name (str): The name of the cube to extract data from.
    """
    dimensions_to_process = CUBE_DIMENSION_MAP.get(cube_name)

    if not dimensions_to_process:
        raise ValueError(f"No dimensions configured for the cube: {cube_name}")

    with TM1Service(**ServerConfig.get_config(environment, instance)) as tm1:
        cube = tm1.cubes.get(cube_name)
        cube_dimensions = cube.dimensions

        # Process only the dimensions specified for this cube
        for dimension_name in cube_dimensions:
            if dimension_name in dimensions_to_process:
                output_file = f"{OUTPUT_DIR}/{dimension_name}.jsonl"
                process_dimension(tm1, dimension_name, cube_name, output_file)


if __name__ == "__main__":
    # Example usage
    extract_data(Environment.DEV, Instance.FINANCE, 'Management Reporting')


--------------------




