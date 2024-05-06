import os
import xml.etree.ElementTree as ET
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def find_files(directory, file_name):
    """ Recursively find all files matching file_name in directory. """
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == file_name:
                yield os.path.join(root, file)

def parse_xml_value(file_path, tag, attribute):
    """ Parse the XML file to extract the value of the specified attribute under the given tag. """
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        for item in root.findall(f".//{tag}"):
            attr_value = item.get(attribute)
            if attr_value and attr_value != '0':  # Ignore entries with no value or placeholder '0'
                return attr_value
    except ET.ParseError as e:
        print(Fore.RED + f"Error parsing XML file: {file_path}. Error: {str(e)}")
        print(Fore.RED + "Unable to read meta file structure, could be a possible crash issue.")
    except Exception as e:
        print(Fore.RED + f"An error occurred: {str(e)}")
        print(Fore.RED + "Unable to read meta file structure, could be a possible crash issue.")
    return None

def main(directory):
    carcols_values = {}
    carvariations_values = {}
    
    # Find and parse carcols.meta files
    for file_path in find_files(directory, 'carcols.meta'):
        value = parse_xml_value(file_path, 'Item', 'value')
        if value:
            if value in carcols_values:
                print(Fore.YELLOW + f"Duplicate ID value found in carcols.meta: {value}")
                print(Fore.YELLOW + f"Locations: {carcols_values[value]} and {file_path}")
            else:
                carcols_values[value] = file_path

    # Find and parse carvariations.meta files
    for file_path in find_files(directory, 'carvariations.meta'):
        value = parse_xml_value(file_path, 'sirenSettings', 'value')
        if value:
            if value in carvariations_values:
                print(Fore.YELLOW + f"Duplicate sirenSettings value found in carvariations.meta: {value}")
                print(Fore.YELLOW + f"Locations: {carvariations_values[value]} and {file_path}")
            else:
                carvariations_values[value] = file_path

if __name__ == "__main__":
    directory = "DIRECTPATHTOVEHCLEFOLDER"
    main(directory)
