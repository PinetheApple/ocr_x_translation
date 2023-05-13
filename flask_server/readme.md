# Flask server

<hr>

## Note

Ensure that all other dependencies are installed

In addition, you will need a Google cloud account to perform the translation:

1. Create a new project in your cloud account
2. Enable the Cloud translation API for the project
3. Under credentials, add a service account with sufficient permissions as required by the API
4. Under your service account, create a new key (or use an existing one) of type JSON. Download the private key to a secure location on your machine.
5. Save the path to your private key file under 'CRED_FILE_PATH'.<br>
   You can do this by using the 'export' command on your terminal.
    ```
    $export CRED_FILE_PATH='path_to_directory/cred_file.json'
    ```

<hr>

## Running the server

Run the following commands in your terminal in the 'flask_server' directory

```
$export FLASK_APP=translation_server'
$flask run
```
