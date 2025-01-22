from finpyalpyn.server.config import ServerConfig, Environment, Instance
from TM1py import TM1Service
from data_extraction.utils import process_dimension


def extract_data(environment: Environment, instance: Instance, cube_name: str):
    """
    Extract data from a specified cube in TM1 and write dimension data to JSONL files.

    Args:
        environment (Environment): The TM1 environment to connect to.
        instance (Instance): The TM1 instance to use.
        cube_name (str): The name of the cube to extract data from.
    """
    with TM1Service(**ServerConfig.get_config(environment, instance)) as tm1:
        cube = tm1.cubes.get(cube_name)
        dimensions = cube.dimensions

        for dimension_name in dimensions:
            process_dimension(tm1, dimension_name, cube_name)


if __name__ == "__main__":
    # Example usage
    extract_data(Environment.DEV, Instance.FINANCE, 'Management Reporting')


----------------

import json


def process_dimension(tm1, dimension_name: str, cube_name: str):
    """
    Process a TM1 dimension, extracting its elements and attributes, and write them to a JSONL file.

    Args:
        tm1 (TM1Service): The TM1Service instance.
        dimension_name (str): The name of the dimension to process.
        cube_name (str): The name of the cube associated with the dimension.
    """
    hierarchy = tm1.dimensions.hierarchies.get(dimension_name, dimension_name)
    elements = hierarchy.elements
    attribute_names = tm1.elements.get_element_attribute_names(dimension_name, dimension_name)

    output_file = f"{dimension_name}.jsonl"
    with open(output_file, "w") as f:
        for element_name, element in elements.items():
            write_element_data(f, cube_name, dimension_name, element_name, "", "")
            for attribute_name in attribute_names:
                attribute_value = element.element_attributes.get(attribute_name, None)
                write_element_data(f, cube_name, dimension_name, element_name, attribute_name, attribute_value)


def write_element_data(file, cube_name: str, dimension_name: str, element_name: str, attribute_name: str, attribute_value):
    """
    Write a single element's data to a JSONL file.

    Args:
        file: The file object to write to.
        cube_name (str): The name of the cube.
        dimension_name (str): The name of the dimension.
        element_name (str): The name of the element.
        attribute_name (str): The name of the attribute (if any).
        attribute_value: The value of the attribute (if any).
    """
    data = {
        "cube_name": cube_name,
        "dimension_name": dimension_name,
        "element_name": element_name,
        "attribute_name": attribute_name,
        "attribute_value": attribute_value,
    }
    file.write(json.dumps(data) + "\n")
