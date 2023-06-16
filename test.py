
import os

 # Get the absolute path of the script
script_path = os.path.realpath(__file__) 

# Get the script directory
script_dir = os.path.dirname(script_path) 
 
print("Script directory:", script_dir)