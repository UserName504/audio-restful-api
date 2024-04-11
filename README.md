# audio-restful-api

A RESTful API, made with [FastAPI](https://fastapi.tiangolo.com/), that allows users to upload, download, and adjust the volume of audio files in Decibel Full Scale (dBFS).

## Setup

Run the following command to build the Docker image:
> ```sh
> $ docker build -t audio-restful-api .
> ```

Afterwards, run the following:
> ```sh
> $ docker compose up --build
> ```

## TESTING:

# /adjust_volume

The use of [Postman](https://www.postman.com/) is recommended for endpoint testing.

To adjust dBFS, the parameters need to be formatted like so:

```json
{
    "input_file": "uploads/AudioExample01.wav",
    "output_file": "uploads/processed_AudioExample01.wav",
    "target_dBFS": -50
}
```

In this example, `processed_AudioExample01.wav` will be added to the `uploads` folder.

# /listfiles

All currently uploaded files can be viewed at `http://127.0.0.1:8000/listfiles/`.

# /downloadfile

Here's an example URL to download a file currently in the uploads folder: 

`http://127.0.0.1:8000/downloadfile/processed_AudioExample01.wav`

## API TESTING:

To test the API endpoints, open the repo in VSCode (or something similar) and run the following:
> ```sh
> $ pytest test_main.py
> ```

## FUTURE WORK:

Next on the list is some kind of front end.