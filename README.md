# National ID Extractor
API for Validating and Extracting Information from National IDs,

Currently, the API supports validation and extraction of information only for Egyptian National IDs.

This version is more concise and professional, clearly stating the functionality of the API and its current scope.

## Features 
    - Flexible Extraction: Supports multiple extraction strategies, allowing the system to process various types of 
      National ID formats (e.g., Egyptian National ID).
      
    - Strategy Pattern: The system uses the Strategy Pattern, where the extraction logic is encapsulated in different classes,
      making it easy to add or modify extraction methods without changing the core logic.

    - Scalable: You can easily add new strategies for extracting information from other ID formats in the future.

    - Service To Service authentication using public & private keys for each customer (service) 
        1- RSA Key Pair Generation: Generate a private and public RSA key pair (2048-bit) for signing and verification.
        
        2- Sign Requests: Sign predefined data (such as a payload) with the private key to ensure 
          data integrity and authenticity.
        
        3- Verify Signatures: Verify a given signature using the public key to confirm that the payload has not been tampered with.

## API Postman Documentation
https://documenter.getpostman.com/view/28439113/2sAYQUqa4N

## Prerequisite
>python


## Installtion & Running Set Up Virtual Environment:
         1-  python -m venv venv.
              source venv/bin/activate  (Linux venv activation)
              venv/scripts/activate     (Windows venv activation)
            
         2- Install Dependencies:: 
             pip install -r requirememnts.txt.
             
         3- Apply Migrations:
           python manage.py migrate.
           
         4- Create Superuser: Required for accessing the admin dashboard. You will be prompted to enter your details:
              python manage.py createsuperuser

         5- To create a service with the necessary authentication keys, simply run the following command:
         
              python manage.py create_service.
             
             This command will generate a new service, automatically creating both a public and private key. 
             It will also sign the private key using the sign_request method from app/utility, 
             then print both the public and the signed private key to the console.

             You can use these keys as request headers for authentication purposes when making API requests.
             

         6- If you wish to create the signed private key in other languages follow these steps:

             - Generate an RSA Key Pair: Use an appropriate RSA key generation method in your language 
               (for example, OpenSSL in C, Java, or Node.js).
             
             - Sign the Payload:
                  Convert the payload into a JSON string (e.g., {"country_code": "EG"}).
                  {"country_code": "EG"} static payload in the code please sign with it.
                  
                  Sign the JSON string with your private key using RSA PSS padding and SHA-256.
                  Encode the resulting signature in base64.
                  
             - Verify the Signature:
                Decode the base64 signature.
                Use the public key (in PEM format) to verify the signature using RSA PSS padding and SHA-256.
                Check if the signature matches the expected result.

              
         7- Run the Development Server:
            python manage.py runserver
            
            The server will be available at http://127.0.0.1:8000. Use the API documentation for testing,
            admin dashboard will be http://127.0.0.1:8000/admin.
            
            You can create as many servicees as you need from admin dashboard,
            public & private keys are created automatically.
            

         8- Run Tests:
            python manage.py test

     
