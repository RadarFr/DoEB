import requests
import os
import base64
import psutil
import uuid

def send_folder_to_server(local_folder, remote_folder, url):
    try:
        folder_contents = []

        folder_name = str(uuid.uuid4())

        # Traverse the local folder recursively and add files to the list
        for root, dirs, files in os.walk(local_folder):
            for file in files:
                local_path = os.path.join(root, file)
                remote_path = os.path.join(remote_folder, folder_name, os.path.relpath(local_path, local_folder))

                with open(local_path, 'rb') as f:
                    file_contents = f.read()
                    file_contents_base64 = base64.b64encode(file_contents).decode('utf-8')
                    file_data = {
                        'name': file,
                        'contents': file_contents_base64
                    }
                    folder_contents.append(file_data)

        remote_folder_path = os.path.join(remote_folder, folder_name)

        # POST data
        payload = {
            'folder_path': remote_folder_path,
            'files': folder_contents
        }
        response = requests.post(url, json=payload)
        response.raise_for_status(

    except requests.exceptions.RequestException as e:
        print(f"Error sending folder: {e}")

def close_application(name):
    for proc in psutil.process_iter():
        if proc.name() == name:
            proc.kill()

def main():
    app_name = "chrome.exe"
    close_application(app_name)
    local_folder = r'C:\Users\Spen\desktop\thingysToSent'
    remote_folder = '/'
    url = "http://127.0.0.1:5000/sendtoapi"

    send_folder_to_server(local_folder, remote_folder, url)

if __name__ == "__main__":
    main()
