import os # V2 EFAR2GTX, this sillo update makes a folder in the output named after the efar, to make sure if there are multiple efar files they dont overwrite eachother, the script re adds the og names and if the index at the end of the file mentions the name with a folder it will create that folder and put the gtx in it.

input_dir = "particle"
output_dir = "rescued" 

header = b'Gfx2'
footer = b'BLK{'

for filename in os.listdir(input_dir):
    if filename.endswith(".efar"):
        file_path = os.path.join(input_dir, filename)
        with open(file_path, "rb") as f:
            data = f.read()
        
        base_name = filename.replace(".efar", "")
        
        efar_output_root = os.path.join(output_dir, base_name)
        
        real_names = []
        current_find_pos = 0
        while True:
            gtx_str_idx = data.find(b".gtx", current_find_pos)
            if gtx_str_idx == -1:
                break
                
            start_str_idx = gtx_str_idx
            while start_str_idx > 0 and data[start_str_idx - 1] >= 32 and data[start_str_idx - 1] < 127:
                start_str_idx -= 1
                
            raw_name_bytes = data[start_str_idx:gtx_str_idx + 4]
            full_path_str = raw_name_bytes.decode('utf-8', errors='ignore')
            
            real_names.append(full_path_str)
            current_find_pos = gtx_str_idx + 4

        texture_positions = []
        parts = data.split(header)
        current_pos = 0
        for i in range(len(parts) - 1):
            current_pos += len(parts[i])
            texture_positions.append(current_pos)
            current_pos += len(header)
            
        if not texture_positions:
            continue

        print(f"Grabbing {filename}: Extracting {len(texture_positions)} textures")

        for i in range(len(texture_positions)):
            start_idx = texture_positions[i]
            
            if i + 1 < len(texture_positions):
                search_limit = texture_positions[i + 1]
            else:
                search_limit = len(data)
                
            end_blk_idx = data.rfind(footer, start_idx, search_limit)
            
            if end_blk_idx != -1:
                mrbuffybuffer = 28 #Due to the nature of this script, it might break n any other game noot wii party u
                end_idx = min(end_blk_idx + len(footer) + mrbuffybuffer, search_limit)
                
                extracted_asset = data[start_idx:end_idx]
                
                if i < len(real_names) and real_names[i]:
                    clean_path = real_names[i].replace('/', '\\')
                    path_parts = clean_path.split('\\')
                    
                    filename_only = path_parts[-1]
                    subfolders = path_parts[:-1]
                    
                    target_folder = os.path.join(efar_output_root, *subfolders)
                    os.makedirs(target_folder, exist_ok=True)
                    
                    save_path = os.path.join(target_folder, filename_only)
                else:
                    os.makedirs(efar_output_root, exist_ok=True)
                    save_path = os.path.join(efar_output_root, f"{base_name}_{i}.gtx")
                    
                with open(save_path, "wb") as out_f:
                    out_f.write(extracted_asset)
                    
                print(f" -> Rescued asset destination: {save_path} ({len(extracted_asset)} bytes)") #Enjoy!
