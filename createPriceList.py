import json
import xml.etree.ElementTree as ET
import os

def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the file {file_path}.")
        return None
        
def find_fillType_fields(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        fillType_values = []
        for fillType in root.findall('.//fillType'):
            fillType_values.append(fillType.text)
        
        return fillType_values
    except ET.ParseError:
        print(f"Error parsing XML from the file {file_path}.")
        return None
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
        return None

def extract_fillType_names(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        names = []
        for fillType in root.findall('.//fillType'):
            name = fillType.get('name')
            if name:
                names.append(name)
        
        return names
    except ET.ParseError:
        print(f"Error parsing XML from the file {file_path}.")
        return None
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
        return None
        
def save_dict_to_json_file(dictionary, file_path):
    try:
        with open(file_path, 'w') as file:
            json.dump(dictionary, file, indent=4)
        print(f"Dictionary successfully saved to {file_path}")
    except IOError as e:
        print(f"An error occurred while writing to the file: {e}")      
          
if __name__ == "__main__":
    file_path = 'settings.txt'
    data_dict = read_json_file(file_path)
    output = {}
    
    if data_dict is not None:
        print("Dictionary read from JSON file:")
        print(data_dict)
        if "gamefile" in data_dict:
            xmlfile = data_dict["gamefile"]
            xmlfile = os.path.expanduser(xmlfile)
            fillType_values = extract_fillType_names(xmlfile)
            if fillType_values is not None:
                print("fillType fields found in the XML file:")
                for value in fillType_values:
                    print(value)
                    output[value] = float(1.0)
                save_dict_to_json_file(output, "prices.txt")
            else:
                print("Failed to read fillType fields from XML file.")
    else:
        print("Failed to read dictionary from JSON file.")
        
        


