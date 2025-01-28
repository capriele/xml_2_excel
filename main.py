import os
import pandas as pd
import xml.etree.ElementTree as ET

def remove_namespace(tag):
    """
    Remove namespace from an XML tag.

    Args:
        tag (str): The tag name with or without namespace.

    Returns:
        str: The tag name without namespace.
    """
    if '}' in tag:
        return tag.split('}', 1)[1]
    '''
    if '_' in tag:
        tags = tag.split('_')
        if len(tags) > 2:
            return tags[-1]
    '''
    return tag

def extract_elements(element, common_data, prefix=""):
    """
    Recursively extract all elements from an XML node, including both leaves and nested elements.

    Args:
        element (xml.etree.ElementTree.Element): The current XML element to process.
        common_data (dict): A dictionary to store extracted data.
        prefix (str): The prefix for nested elements (to track hierarchy).

    Returns:
        None
    """
    tag = remove_namespace(element.tag)
    full_tag = prefix + tag
    full_tag = remove_namespace(full_tag)
    if full_tag not in common_data:
        common_data[full_tag] = []
    common_data[full_tag].append(element.text)

    # If the element has children, recurse through its children
    for child in element:
        new_prefix = prefix + tag + "_"
        extract_elements(child, common_data, new_prefix)

def parse_xml_to_dataframe(xml_file):
    """
    Parse the XML file and convert it to a pandas DataFrame.
    All elements are treated as separate columns.

    Args:
        xml_file (str): Path to the XML file.

    Returns:
        pd.DataFrame: Data extracted from the XML file.
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()

    common_data = {}

    # Extract all elements recursively
    extract_elements(root, common_data)

    # Convert the dictionary to a DataFrame
    max_length = max(len(v) for v in common_data.values())
    for key in common_data:
        if len(common_data[key]) < max_length:
            common_data[key].extend([None] * (max_length - len(common_data[key])))

    return pd.DataFrame(common_data)

def save_to_excel(dataframe, output_file):
    """
    Save the DataFrame to an Excel file.

    Args:
        dataframe (pd.DataFrame): DataFrame to save.
        output_file (str): Path to the Excel file.
    """
    dataframe.to_excel(output_file, index=False)

def main():
    import sys

    if len(sys.argv) != 2:
        print("Usage: python xml_to_excel.py <xml_file>")
        return

    input_file = sys.argv[1]
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = os.path.join(os.path.dirname(input_file), f"{base_name}.xlsx")

    dataframe = parse_xml_to_dataframe(input_file)
    save_to_excel(dataframe, output_file)
    print(f"Excel file saved to {output_file}")

if __name__ == "__main__":
    main()