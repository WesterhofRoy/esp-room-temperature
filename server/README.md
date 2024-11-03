# Server

This server is deployed to Google Cloud using App Engine.

## Running the server

### Setting up the environment

1. Install python3(.11) and pip3
2. Make sure your terminal is in the server directory
3. run:  
    ```shell
    py -m venv venv
    .\venv\Scripts\Activate
    pip install -r requirements.txt
    ```

### Running the server

1. Make sure your terminal is in the server directory and the environment is activated:  
    - To know if the environment is activated, the terminal should have `(venv)` at the beginning of the line.  
        You can also run the following command to check if the environment is activated:  
        ```shell
        pip -V  # Note: Capital V
        ```
    - To activate the environment, run:  
        ```shell
        .\venv\Scripts\Activate
        ```
2. Run the server:
    ```shell
    uvicorn src.main:app --host 0.0.0.0 --port 8080 --log-level debug
    ```
3. Open your browser and go to `http://localhost:8080/docs` to see the API documentation.
