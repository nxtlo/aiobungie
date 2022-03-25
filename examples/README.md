# aiobungie Examples

The examples listed in each file demonstrate different use cases of the library.

## Running Examples
To run an example you'll first need:
    - This lib installed with its requirements.
    - An API key from Bungie developer portal application.

Some example may require more information, Like the `user_oauth` example,
This will require an SSL certificate to be able to run the authentication web server on HTTP.

Also another example in `transfer_items` will require your actual characters IDs and used within your OAuth2 implementation flow.

After setting up everything in the chosen example simply run:
```py
python example_file.py
```

## Examples List
```
1: hello_world => A very basic client that fetch our player memberships, find the Steam one, and then print information about it and its character equipments.
2: manifest => Manifest usage example for both SQLite and JSON formats.
3: transfer_items => Transfer your items from a character to another.
4: user_oauth2 => Full implementation on OAuth2 workflow.
```

### Contributing
More examples are welcomed to PRd, Just make sure you test them and include the information about
the example in the format above.

### Questions and Issues
If you have any question or encountered and error when running one of the examples, Feel free to open
an Issue.