
from imghst.app.configuration.unique_generators.uuid_based import generate_unique_id
from pathlib import Path

class Configuration:
    """ Do all configuration stuff here. """
    
    api_request_key = "InsertKeyHere"
    image_unique_file_name = generate_unique_id
    image_hosting_folder = Path("/home/mustafa/Development/imghst/images")
    
    port_number_to_run_on = 5000
