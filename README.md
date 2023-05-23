Is an API that allows users to save screenshots in the cloud and set up access and sharing policies.

The web framework here will use Fastapi
from AWS is used here:
- S3 buckets
- Cognito
- API Gateway
- Lambda
- DynamoDB

To deploy this project, you need:
- install AWS CLI and SAM CLI
- set up your credentials in `.aws/credentials`
- build this project: `sam build`
- deploy this project `sam deploy --guided`