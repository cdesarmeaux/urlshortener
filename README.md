# urlshortener
Microservice to shorten URLs written in Python (Falcon) and containerizable
### How it works
* For POST requests, the service takes in a JSON body with the URL to shorten. It appends the URL to a table in a simple sqlite3 database file, and returns the a shortened url: the ID of the database record just created encoded to base 62. If the URL passed in the request body already exists, then the ID of the corresponding record will be encoded and returned.
* For GET requests, the service will simply take the shortened URL and decode it back to base 10, use the result as to search the databse by ID, and redirect the user to the URL associated with the ID.

The service takes care of all error handling (invalid URL, unexisting IDs, etc...). For scalability, it runs behind an nginx proxy server. The nginx server simply proxies requests to the WSGI server. Thus the tester will only need to call the nginx server.

### How to run
The service can run either with a docker container or directly with a python web server gateway interface.
For simplicity, I will describe how to run the service with docker, as it will avoid building a whole runtime in a non-isolated environment. There are 2 containers: one for the app server, and one for the nginx server. The following instructions describe how to run the service on port 8000:
1. First of all, the machine running the service should have docker installed and running. [Instructions about how to install and run docker here](https://docs.docker.com/install/#upgrade-path). Since there will be 2 containers running, we will be using the `docker-compose` command to run the service, which is a seperate tool to be installed for __Linux users only__ (it is automatically installed on Mac and Windows)
2. Unzip the source code folder if it hasn't been cloned from github
3. Open a terminal window (or a cmd prompt/powershell for Windows users).
4. Navigate to the directory where you have cloned/downloaded the project (you should be at the level where you have the `docker-compose.yml` file
5. Make sure you have root privileges (necessary for Linux users)
6. Make sure port 8000 is not in use
7. Run the following command:  `docker-compose up -d`. This will download all dependencies, build the docker images and run them.
8. Open an API testing tool, like Postman, and make your requests to `http://localhost:8000/`, you can now use the service the same way as the description

### How to scale
The WSGI server chosen to serve the app is gunicorn because it handles concurreny very well. Since the application heavily relies on database read/write operations, I have decided to run gunicorn as an asynchronous/non-blocking server. Such a server relies on an I/O loop to handle concurrency: a thread being blocked by an I/O operation (in this case a database call) will not go to sleep, it will instead expect a callback function from the I/O operation, and move on to other tasks in the meantime. This allows great performance, and uses less memory than a synchronous server (which would just spawn new threads to overcome the I/O bottlenecks).
 
 The gunicorn server is then configured to duplicate itself into different processes for extra concurrency. The number of processes is the result of a function of the number of cpu cores in the host machine. This way, scaling up (getting more powerful hardware) is handled automatically.
 
 In front of gunicorn lies an nginx server. Nginx stands out with a sophisticated event‑driven architecture that enables it to scale to hundreds of thousands of concurrent connections because it uses asynchronous handling of requests (similar to the WSGI configuration). To gain even more performance under high traffic, nginx also relieves the WGSI server from those tasks:
 * microcaching
 * TLS termination
 * response buffering for slow clients
 
If the service needs to scale out, a good approach would be to run it on multiple (virtual) machines. The ease of deployment of a container is handy for that purpose, as duplicating the containers in a cluster of servers is a great solution for scalability. Added to that, nginx is capable of handling load balancing, and can evenly dispatch incoming requests to running containers on multiple machines.

Another step to scale would be to use a databse server. In this microservice, for convieniance I have used sqlite3, which is serverless. Although sqlite3 managed to handle some concurrency for the db file access, it is nowhere near the performance of a more robust database server, which could run in its own container in order to have it's own level of scalability.