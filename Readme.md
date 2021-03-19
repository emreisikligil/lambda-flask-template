# Lambda Flask Template

This is a template for configuring and deploying Flask apps on AWS Lambda.

## Template Modules

### Application

All application modules are located under **application** package. Rename this package as you see fit. It is the main package of your application.

`__init__.py`: Entry point of the main package. Contains flask app factory method. Also includes **Application** class that keeps objects that might be needed.

`__main__.py`: Module to enable to run the application as a module (`python -m application`).

`config.py`: Contains application configurations. Configurations are set through environment variables.

`exceptions.py`: Add applications exceptions here.

`models.py`: Contains SQLAlchemy models. Add your database models here.

`views.py`: Contains Flask API views. Add views for your API endpoints here.

### Testing

Test modules are located under **tests** folder. **pytest** package is used for testing. Add new modules here as you need to add tests for different modules.

`__init__.py`: Make tests folder a package

`conftest.py`: Contains some pytest fixtures. Your fixtures are processed by pytest automatically when you add them here.

`test_views.py`: Add your tests for API views here. It contains 2 sample tests.

### Migrations

This folder contains database migration scripts and managed by Flask-Migrate package. Initial migration script already exists to be a sample. You can remove it from version folder for the sake of your own database models.

## Dependencies

- Python 3.8
- Python packages

  ```bash
  pip install -r requirements.txt
  ```

  If you would like to install and run in a virtual environment

  ```bash
  python -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  ```

  After you are done with the virtual environment

  ```bash
  deactivate
  ```

- **[node.js](https://nodejs.org/en/)**: npm comes with node.js
- Serverless with required plugins for deployment
  ```
  npm install -g serverless
  npm install --save serverless-python-requirements serverless-wsgi serverless-domain-manager
  ```
- `swagger-cli` tool for derefencing swagger spec for validators to process incoming requests
  ```
  npm install -g swagger-cli
  ```
- `redoc-cli` in order to generate api docs
  ```
  npm install -g redoc-cli
  ```

## How to Use This Template

1. Add necessary configuration properties to **config.py**. Some properties are added by default. Check [Flask](https://flask.palletsprojects.com/en/1.1.x/config) for more configuration options.

   **TESTING**: Set this to True when testing

   **SQLALCHEMY_DATABASE_URI**: Database connection URI

   **RSA_PUBLIC_KEY**: RSA public key to validate JWT in case you use [flaskjwt](https://github.com/emreisikligil/python-utils#flaskjwt) module.

1. Create your database models under **application.models** package.
1. Create initial migration for your database

   1. Create migrations folder. You can skip this step if **migrations** folder exists. Make sure **versions** folder is empty.

      ```sh
      flask db init
      ```

   1. Create initial migration

      ```sh
      flask db migrate -m "Initial migration"
      ```

   1. Check if the migration script created under **migrations/versions** is correct.
   1. Apply migrations to the database. **WARNING:** This will apply changes to the database pointed by _SQLALCHEMY_DATABASE_URI_ configuration property.

      ```sh
      flask db upgrade
      ```

1. Edit swagger spec to match your API. This will be used for validating incoming request bodies automatically. If you do not want to use this feature you can skip this step and remove **spec** folder.

   1. Put your spec to `application/spec/swagger.yml`. JSON objects to be validated must be defined under **definitions**.
   1. Run `make deref-spec` in order to dereference the refs in the spec. Validator does not dereference them automatically yet.

1. Create API documentation from swagger.yml.

   ```sh
   make doc
   ```

   which will create **docs/index.html**. Then you can serve this file from Flask with

   ```python
   from werkzeug.exceptions import NotFound
   from flask import send_file

   @app.route("/spec", methods=["GET"])
   def apidocs():
       filename = join(dirname(__file__), "../docs/index.html")
       if not exists(filename):
           raise NotFound("API documentation not found")
       return send_file(filename)
   ```

1. Edit Flask views to handle incoming requests. You can use request body validation and authenticate incoming request with jwt.

   ```python
   from pyutils.auth.flaskjwt import FlaskJWT, Claims
   from pyutils.schema_validation import SchemaValidation

   app = Flask()
   auth = FlaskJWT("key", ["RS256"])
   schema = SchemaValidation("spec/swagger-flat.yml")

   @app.route("/pets", methods=["POST"])
   @auth.authenticated
   @schema.validate("AddPetRequest")
   def add_pet(add_pet_request, claims: Claims):
       # add_pet_request is validated and contains the input as dict.
   ```

1. Test your application

   1. Add tests to cover your application
   1. Run your tests.

      ```sh
      pytest tests
      ```

## Run Locally

1. Add your configuration properties to the environment

   ```sh
   export SQLALCHEMY_DATABASE_URI=postgresql://username:password@domain.com/database
   export RSA_PUBLIC_KEY="..."
   ```

2. Run the application

   ```sh
   python -m application
   ```

   or

   ```sh
   export FLASK_APP=application.app
   python -m flask run
   ```

## Deploy to AWS Lambda

We use [Serverless](https://www.serverless.com/) to deploy the application to the AWS Lambda.

1. Edit **serverless.yml**

   1. Update service name

      ```yaml
      service: your_application_name
      ```

   1. Edit configuration properties under `provider.environment`. Configuration properties are fetched from AWS SSM Parameter Store. Therefore, you need to add your configuration properties to SSM Parameter Store before deploying the application.

      E.g. if you have the following configuration property

      ```yaml
      SQLALCHEMY_DATABASE_URI: ${ssm:/${self:provider.stage}/application/db~true}
      ```

      Then, you need to have following parameters in the Parameter Store:

      ```
      /prod/application/db
      /staging/application/db
      /dev/application/db
      ```

   1. If you are planning to use a S3 bucket, then you need to check/update the following items. Otherwise, you can delete them.

      `provider.s3`: Creates the S3 bucket.

      `provider.iamRoleStatements`: Grants permissions to the lambda function for access to the created bucket

      `resources.Resources.s3Policy`: In case you need additional policy for the created s3 bucket

   1. To create an API Gateway endpoint, check/update `custom.domains` and `custom.customDomain` keys. Serverless plugin (_serverless-domain-manager_) will handle API Gateway endpoint creation.

   1. You need to update `custom.vpc` key in order to place the lambda function in a specific VPC. Otherwise, you need to remove `provider.vpc` and `custom.vpc`.

   1. If you make any changes to the application package you need to reflect these changes to `custom.wsgi.app` key. It is how wsgi server finds your Flask application.

   1. `custom.pythonRequirements` key configures _serverless-python-requirements_ plugin. Edit if necessary.

1. Run the following command. It uses the default aws account. This account needs to have the necessary permissions to perform operations listed under **serverless.yml**

   ```sh
   serverless deploy -s stage
   ```

   where **stage** is one of _dev, staging, prod_

## Makefile

The project includes a Makefile to make it easier to run some commands. It has the following commands.

```sh
make deploy-prod
make deploy-staging
make deploy-dev
make run
make test
make deref-spec
make doc
```
