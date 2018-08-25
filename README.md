# urlshortener
Microservice to shorten URLs written in Falcon and containerizable

## How it works
* For post requests, the service takes in a JSON body with the URL to shorten. It appends to the URL to a table in a simple sqlite3 database file, and returns the ID of the database record just created encoded to base 62. If the URL passed already exists, then the ID of the corresponding record will be encoded.
* For get requests, the service will simply take the shortened URL and decode it back to base 10, use the result as to search the databse by ID, and redirect the user to URL associated with the ID.

The service takes care of all error handling (invalid URL, unexisting IDs, etc...)

## How to run


## How to scale
