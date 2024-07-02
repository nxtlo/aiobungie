# aiobungie Examples

The examples listed in each file demonstrate different use cases of the library.

## Running Examples

To run an example you'll first need:

* This lib installed with its requirements.
* An API key from Bungie developer portal application.

Some examples may require more information, Like the `user_oauth` example,
This will require an SSL certificate to be able to run the authentication web server on HTTPS.

Also some other examples will require your actual characters/membership IDs.

After setting up everything in the chosen example simply run:

```sh
python example_file.py
```

## Examples List

```s
1: hello_world:    A simple example on how to use aiobungie client.
2: manifest:       Manifest usage example for both SQLite and JSON database.
3: transfer_items: Transfer your items from a character to another.
4: user_oauth2:    Full implementation on OAuth2 workflow.
5: request:        Example on how to use aiobungie framework only with requests in non-async code.
6: error_handling: Using aiobungie exceptions to handle errors.
7: caching:        Using aiobungie client metadata to store objects to avoid making HTTP requests multiple times.
```

### Contributing

More examples are welcomed to PRd, Just make sure you test them and include the information about
the example in the format above.

### Questions and Issues

If you have any question or encountered and error when running one of the examples, Feel free to open
an Issue.
