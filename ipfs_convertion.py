import json
import os
import subprocess

def add_to_ipfs(filepath):
    from pathlib import Path
    import requests

    # Ensure the path is handled correctly on Windows
    filepath = Path(filepath)
    
    # Open file in binary read mode
    with filepath.open("rb") as fp:
        files = {"file": (filepath.name, fp)}
        
        # POST request to IPFS
        url = "http://127.0.0.1:5001/api/v0/add"
        

        try:
            # Run a command that might fail
            result = subprocess.run(['ipfs', 'add', filepath], capture_output=True, text=True, check=True)
            output = result.stdout.strip()
            print(f"Command output: {output}")
            

            
            parts = output.split()
            if len(parts) >= 2:
                cid = parts[1]
                print(f"File added with CID: {cid}")
                url = f"https://ipfs.io/ipfs/{cid}"

                print("Public URL: ", url)
            else:
                print("Unexpected output format")
        except subprocess.CalledProcessError as e:
            print(f"Command failed with return code {e.returncode}")
            print(f"Error output: {e.stderr}")

    return cid


def main():

    json_file_path='output_path.json'

    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as file:
            file_paths = json.load(file)
    else:
        file_paths = {"video_paths": []}

    # Process each video path
    for entry in file_paths['video_paths']:
        if not entry['isHashed']:  # Check if the path has already been hashed
            ipfs_hash = add_to_ipfs(entry['path'])
            entry['hash'] = ipfs_hash  # Update the hash
            entry['isHashed'] = True   # Mark as hashed

    with open(json_file_path, 'w') as file:
        json.dump(file_paths, file, indent=12)
    
    print("IPFS hashes generated and updated where needed.")
                            
if __name__ == "__main__":
    main()

