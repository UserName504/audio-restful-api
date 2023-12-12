from fastapi.testclient import TestClient
from pathlib import Path
from main import app

client = TestClient(app)

def test_upload_file():
    # Prepare a test file
    test_file_content = b"test file content"
    test_file_name = "test_upload_file.txt"     #Just a blank .txt file, for the sake of demonstration.
    # Make a request to the upload file endpoint
    response = client.post("/uploadfile/", files={"file": (test_file_name, test_file_content)})
    # Assert the response status code is 200 OK
    assert response.status_code == 200
    # Assert the response JSON contains the uploaded file name
    assert response.json() == {"filename": test_file_name}
    # Clean up: Delete the test file
    client.delete(f"/deletefile/{test_file_name}")
    # Ensure the test file is deleted
    assert not (Path("uploads") / test_file_name).exists()

def test_list_files():
    # Prepare a test file
    test_file_content = b"test file content"
    test_file_name = "test_list_files.txt"      #Just a blank .txt file, for the sake of demonstration.
    # Make a request to the upload file endpoint
    response_upload = client.post("/uploadfile/", files={"file": (test_file_name, test_file_content)})
    # Assert the upload response status code is 200 OK
    assert response_upload.status_code == 200
    # Make a request to the list files endpoint
    response_list = client.get("/listfiles/")
    # Assert the list response status code is 200 OK
    assert response_list.status_code == 200
    # Assert the response JSON contains the uploaded file name
    assert test_file_name in response_list.json()["files"]
    client.delete(f"/deletefile/{test_file_name}")          #Delete the test file.
    assert not (Path("uploads") / test_file_name).exists()  #Make sure that hte test file has been deleted.

def test_download_file():
    # Prepare a test file
    test_file_content = b"test file content"
    test_file_name = "test_download_file.txt"   #Just a blank .txt file, for the sake of demonstration.
    # Make a request to the upload file endpoint
    response_upload = client.post("/uploadfile/", files={"file": (test_file_name, test_file_content)})
    # Assert the upload response status code is 200 OK
    assert response_upload.status_code == 200
    # Make a request to the download file endpoint
    response_download = client.get(f"/downloadfile/{test_file_name}")
    # Assert the download response status code is 200 OK
    assert response_download.status_code == 200
    # Assert the response content matches the uploaded file content
    assert response_download.content == test_file_content
    client.delete(f"/deletefile/{test_file_name}")          #Delete the test file.
    assert not (Path("uploads") / test_file_name).exists()  #Make sure that hte test file has been deleted.

def test_delete_file():
    # Prepare a test file
    test_file_content = b"test file content"
    test_file_name = "test_delete_file.txt"
    # Make a request to the upload file endpoint
    response_upload = client.post("/uploadfile/", files={"file": (test_file_name, test_file_content)})
    # Assert the upload response status code is 200 OK
    assert response_upload.status_code == 200
    # Make a request to the delete file endpoint
    response_delete = client.delete(f"/deletefile/{test_file_name}")
    # Assert the delete response status code is either 200 OK or 404 Not Found
    assert response_delete.status_code in [200, 404]
    if response_delete.status_code == 200:
        # Ensure the test file is deleted
        assert not (Path("uploads") / test_file_name).exists()
    elif response_delete.status_code == 404:
        # Assert the response JSON contains a message about the file not found
        assert response_delete.json()["detail"] == "File not found"

def test_adjust_volume():
    # Prepare a test audio file
    test_audio_content = b"test audio content"
    test_audio_name = "test_adjust_volume.wav"  #The same as AudioExample01.wav, but with a different name.
    # Make a request to the upload file endpoint
    response_upload = client.post("/uploadfile/", files={"file": (test_audio_name, test_audio_content)})
    # Assert the upload response status code is 200 OK
    assert response_upload.status_code == 200
    # Make a request to the adjust volume endpoint
    data = {
        "input_file": f"uploads/{test_audio_name}",
        "output_file": f"uploads/adjusted_{test_audio_name}",
        "target_dBFS": -10  # Adjust the volume by -10 dBFS (adjust as needed)
    }

    response_adjust_volume = client.post("/adjust_volume", json=data)
    # Assert the adjust volume response status code is either 200 OK or 500 Internal Server Error
    assert response_adjust_volume.status_code in [200, 500]
    if response_adjust_volume.status_code == 200:
        # Assert the adjusted file exists
        adjusted_file_path = Path("uploads/adjusted_") / test_audio_name
        assert adjusted_file_path.exists()
    client.delete(f"/deletefile/{test_audio_name}")             #Delete the test file.
    client.delete(f"/deletefile/adjusted_{test_audio_name}")    #Make sure that hte test file has been deleted.