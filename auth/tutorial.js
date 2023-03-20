//* requirements
// command: pip install PyJWT
// for encoding and decoding JWT tokens
// command: pip install python-decouple
// for reading environment variables

//* generating secret
// from built in python module secrets, use the function secrets.token_hex(n) to generate hex string of n characters

//* select algorithm
// choose an algorithm for decoding and encoding JWT

//* create handlers
// create functions for encoding and decoding JWT
//! create signin and login functions

//* define jwt_bearer
// for authorizing the user for specific requests

//* use jwt_bearer class
// import Depends from fastapi and use the below aregument to any post or get request as dependencies
//! dependencies=[Depends(jwtBearer())]

//= there will be a lock on URLs authorized

//= Github link for source code
// https://github.com/BekBrace/FASTAPI-and-JWT-Authentication/blob/main/main.py
