# Project Assignment
You have been tasked with building a Python app that retrieves input in structured JSON (the 
format of which is to your choosing), validates the input, logs the input to STDOUT, and 
sends a request (the format of which is to your choosing) to a HTTP based API, with the 
input being part of the request message.

## Guidance
* Provide a detailed walk through of your thought process to understand any 
architectural & other considerations, that help you arrive at a proposed solution 
* Provide a descriptive overview of the the solution 
* Document challenges, considerations, requirements

## Notes
* We don’t expect you to provide a compiled app, however, the codebase must be compilable
  * Feel free to provide the codebase as a file, or as a Git repository
  * You can also provide a Go Playground link, if you prefer
* Feel free to provide diagrams, and other material, as relevant to support your response

### Requirements
runtime: python3.10
install requirements: 

```pip install -r requirements.txt```

### How to run

Keyword arguments are optional
`python app.py --host '127.0.0.1' --port 5000 --debug`

Endpoint can be invoked via curl with the following command:
```
curl --header "Content-Type: application/json" --request POST --data \
 '{"name":"tobias","dob": "1987-03-10"}' http://localhost:5000/sender
```

It is expected that the received JSON will be printed to STDOUT
It is expected that the sender endpoint sends a request to the receiver endpoint which contains
a JSON object that includes the initial request message. 
It is expected that the receiver endpoint, when executed without issues, prompts the sender endpoint to 
return a response message with `{"success": true}`

### How to unittest

```pytest test_app.py```

Additional test and code documentation can be found inside app.py and test_app.py