import requests
import os
import mimetypes

def download_image(image_url:str, download_folder:str, filename:str):
    try:
        response = requests.get(image_url)
        
        if response.status_code == 200:
            
            content_type = response.headers.get("Content-Type", 'image/jpeg')
            file_extension = mimetypes.guess_extension(content_type) or ".jpg"
            file_name = str(filename) + file_extension
            
            with open(os.path.join(download_folder, file_name), 'wb') as image:
                image.write(response.content)
            print(f"{file_name} Downloaded to {download_folder}")
            
            return True
    
    except:
        print(f"Image {filename} failed to download")
        return False
    
    print(f"Image {filename} failed to download")
    return False
