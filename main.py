import json
from typing import Any

import jinja2
from flamapy.core.discover import DiscoverMetamodels
#from flamapy.metamodels.configuration_metamodel.models import Configuration


class Configuration:

    def __init__(self, elements: dict[str, Any] = {}) -> None:
        self.elements = elements

    def is_selected(self, element: str) -> bool:
        return element in self.elements and self.elements[element]
    
    def get_value(self, element: str) -> Any:
        return self.elements[element]


def load_configuration_from_file(filepath: str) -> Configuration:
    with open(filepath) as file:
        json_dict = json.load(file)
    config = json_dict['config']
    return Configuration(config)


if __name__ == '__main__':
    # Initialization of Flamapy
    dm = DiscoverMetamodels()

    # Initialization of Jinja
    template_loader = jinja2.FileSystemLoader(searchpath="icecream/templates")
    environment = jinja2.Environment(loader=template_loader, trim_blocks=True, lstrip_blocks=True)

    # Step 1. Load the FM
    fm = dm.use_transformation_t2m('icecream/fm_models/icecream_fm.uvl', 'fm')

    # Step 2. Load a configuration of the FM
    config = load_configuration_from_file('icecream/configurations/icecream_fm_cone.uvl.json')
    print(config.elements)
    #config.elements['Flavors'].pop()
    # Step 2 (alternative). Generate a random configuration

    # Step 3. Load the templates
    template = environment.get_template('icecream_template.txt.jinja')

    # Step 4. Generate the product from the configuration
    content = template.render(config.elements)
    print(content)
    # Save the product
    with open('product.txt', 'w', encoding='utf-8') as file:
        file.write(content)

