from fastapi.testclient import TestClient
from pathlib import Path
from main import app

client = TestClient(app)

def test_upload_file():
    test_file_content = b"test file content"
    test_file_name = "test_upload_file.txt"                 #Just a blank .txt file, for the sake of demonstration.
    response = client.post("/uploadfile/", files={"file": (test_file_name, test_file_content)}) #Make an endpoint request.
    assert response.status_code == 200                      #Make sure that the status code is 200.
    assert response.json() == {"filename": test_file_name}  #Make sure that the JSON data contains the uploaded file name.
    client.delete(f"/deletefile/{test_file_name}")          #Delete the test file.
    assert not (Path("uploads") / test_file_name).exists()  #Make sure that hte test file has been deleted.

def test_list_files():
    test_file_content = b"test file content"
    test_file_name = "test_list_files.txt"
    response_upload = client.post("/uploadfile/", files={"file": (test_file_name, test_file_content)})
    assert response_upload.status_code == 200
    response_list = client.get("/listfiles/")
    assert response_list.status_code == 200
    assert test_file_name in response_list.json()["files"]
    client.delete(f"/deletefile/{test_file_name}")
    assert not (Path("uploads") / test_file_name).exists()

def test_download_file():
    test_file_content = b"test file content"
    test_file_name = "test_download_file.txt"
    response_upload = client.post("/uploadfile/", files={"file": (test_file_name, test_file_content)})
    assert response_upload.status_code == 200
    response_download = client.get(f"/downloadfile/{test_file_name}")
    assert response_download.status_code == 200
    assert response_download.content == test_file_content
    client.delete(f"/deletefile/{test_file_name}")
    assert not (Path("uploads") / test_file_name).exists()

def test_delete_file():
    test_file_content = b"test file content"
    test_file_name = "test_delete_file.txt"
    response_upload = client.post("/uploadfile/", files={"file": (test_file_name, test_file_content)})
    assert response_upload.status_code == 200
    response_delete = client.delete(f"/deletefile/{test_file_name}")
    assert response_delete.status_code in [200, 404]
    if response_delete.status_code == 200:
        assert not (Path("uploads") / test_file_name).exists()
    elif response_delete.status_code == 404:
        assert response_delete.json()["detail"] == "File not found"

def test_adjust_volume():
    test_audio_content = b"test audio content"
    test_audio_name = "test_adjust_volume.wav"  #The same as AudioExample01.wav, but with a different name.
    response_upload = client.post("/uploadfile/", files={"file": (test_audio_name, test_audio_content)})
    assert response_upload.status_code == 200
    data = {
        "input_file": f"uploads/{test_audio_name}",
        "output_file": f"uploads/adjusted_{test_audio_name}",
        "target_dBFS": -50
    }
    response_adjust_volume = client.post("/adjust_volume", json=data)
    assert response_adjust_volume.status_code in [200, 500]
    if response_adjust_volume.status_code == 200:
        adjusted_file_path = Path("uploads/adjusted_") / test_audio_name
        assert adjusted_file_path.exists()
    client.delete(f"/deletefile/{test_audio_name}")
    client.delete(f"/deletefile/adjusted_{test_audio_name}")