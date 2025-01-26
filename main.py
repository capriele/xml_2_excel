# xml_to_excel.py
import os
import pandas as pd
import xml.etree.ElementTree as ET
import sys

def xml_to_excel(xml_file):
    """
    Convert an XML file to an Excel file.

    Args:
        xml_file (str): Path to the XML file.
    """
    try:
        # Parse the XML file
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Extract data from XML
        data = []
        columns = set()
        
        for element in root:
            row_data = {}
            for subelement in element:
                row_data[subelement.tag] = subelement.text
                columns.add(subelement.tag)
            data.append(row_data)

        # Create a DataFrame
        df = pd.DataFrame(data, columns=list(columns))

        # Determine output Excel file path
        base_name = os.path.splitext(os.path.basename(xml_file))[0]
        excel_file = os.path.join(os.path.dirname(__file__), f"{base_name}.xlsx")

        # Save DataFrame to Excel
        df.to_excel(excel_file, index=False)
        print(f"Successfully converted {xml_file} to {excel_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python xml_to_excel.py <xml_file>")
    else:
        xml_file = sys.argv[1]
        xml_to_excel(xml_file)
