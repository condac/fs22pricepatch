import xml.etree.ElementTree as ET
import json
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
        
def update_price_per_liter(file_path, factors_dict):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        for fillType in root.findall('.//fillType'):
            name = fillType.get('name')
            if name in factors_dict:
                factor = factors_dict[name]
                economy = fillType.find('economy')
                if economy is not None:
                    price_per_liter = float(economy.get('pricePerLiter', '0'))
                    updated_price = price_per_liter * factor
                    economy.set('pricePerLiter', str(updated_price))
        
        tree.write('updated_data.xml', encoding='utf-8', xml_declaration=True)
        print("XML file successfully updated and saved as 'updated_data.xml'")
    except ET.ParseError:
        print(f"Error parsing XML from the file {file_path}.")
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Dictionary with factors
    factors_dict = {
        "WHEAT": 1.0,
        "BARLEY": 1.0,
        "OAT": 1.0,
        "CANOLA": 1.0
    }
    file_path = 'settings.txt'
    data_dict = read_json_file(file_path)
    factors_dict = read_json_file("prices.txt")

    # File path of the input XML file
    file_path = 'data.xml'
    if data_dict is not None:
        print("Dictionary read from JSON file:")
        print(data_dict)
        if "gamefile" in data_dict:
            xmlfile = data_dict["gamefile"]
            xmlfile = os.path.expanduser(xmlfile)
            # Call the function to update the XML file
            update_price_per_liter(xmlfile, factors_dict)