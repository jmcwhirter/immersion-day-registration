
__Setup:__
1. Create a DynamoDB table to collect e-mails
``` bash
aws dynamodb create-table --table-name registrations --attribute-definitions AttributeName=name,AttributeType=S AttributeName=email,AttributeType=S --key-schema AttributeName=email,KeyType=HASH AttributeName=name,KeyType=RANGE --billing-mode PAY_PER_REQUEST
```
2. Deploy the app to your own account
``` bash
zappa deploy dev
```
3. Take the deployment endpoint from Zappa and init first:

   https://WHATEVER_YOUR_ENDPOINT_IS.amazonaws.com/dev/init

4. Once that finishes you'll be redirected to the home page

   _If your CSS doesn't show, it's because FlaskS3 set a metadata tag incorrectly. Change the mime type from binary/octet-stream to text/css in the console (until I can write some code to do it via CLI)._
5. Verify things work by submitting a registration:

   https://WHATEVER_YOUR_ENDPOINT_IS.amazonaws.com/dev/


__Usage:__
1. Query DynamoDB for e-mails. This will output as
``` bash
aws dynamodb scan --table-name registrations --query 'Items[*].email' --output text
```
2. Provide the list of e-mails here:

   https://www.qwiklabs.com/my_account/token_allocation_groups


__Clean-up:__
1. Delete DynamoDB table
``` bash
aws dynamodb delete-table --table-name registrations
```
2. Undeploy Flask app
``` bash
zappa undeploy dev
```
