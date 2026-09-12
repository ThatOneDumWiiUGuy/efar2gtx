import os

input_dir = "effect"
output_dir = "rescued" #Make sure you have these folders, otherwise it will crash! Or alternitviley, change it to a folder you do have.

header = b'Gfx2'
footer = b'BLK{'

for filename in os.listdir(input_dir):
    if filename.endswith(".efar"):
        file_path = os.path.join(input_dir, filename)
        with open(file_path, "rb") as f:
            data = f.read()
        
        base_name = filename.replace(".efar", "")
        
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

                mrbuffybuffer = 28 # Is this a very botched way of doing this? Yes.
                end_idx = min(end_blk_idx + len(footer) + mrbuffybuffer, search_limit)
                
                extracted_asset = data[start_idx:end_idx]
                
                output_name = f"{base_name}_{i}.gtx"
                with open(os.path.join(output_dir, output_name), "wb") as out_f:
                    out_f.write(extracted_asset)
                    
                print(f" -> Saved to output folder: {output_name} ({len(extracted_asset)} bytes)") # If this script doesn't work, Then contact meh! This was designed for Wii Party U, so if other games use this it might not work.
