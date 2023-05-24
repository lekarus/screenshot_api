Is an API that allows users to save screenshots in the cloud and set up access and sharing policies.

The web framework here will use [Fastapi](https://fastapi.tiangolo.com/)

From AWS is used here:
- [S3 buckets](https://docs.aws.amazon.com/s3/index.html)
- [Cognito](https://docs.aws.amazon.com/cognito/index.html)
- [API Gateway](https://docs.aws.amazon.com/apigateway/index.html)
- [Lambda](https://docs.aws.amazon.com/lambda/index.html)
- [DynamoDB](https://docs.aws.amazon.com/dynamodb/index.html)

To deploy this project, you need:
- install [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) and [SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
- set up your [credentials](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html) in `.aws/credentials`
- build this project: `sam build`
- deploy this project `sam deploy --guided`

For local deployment you can use:
- `sam local start-lambda` to deploy Lambda locally
- `sam local start-api` to deploy APIGateway locally 
