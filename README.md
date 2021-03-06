### Prerequisites:
- Python 2.7
  - Mac: `brew install python@2`
- AWS CLI
  - Mac: `brew install awscli`
- JQ library
  - Mac: `brew install jq`
- Zappa is configured to deploy to US-East-2
  - `aws configure set default.region us-east-2` OR
  - Add `--region us-east-2` to your DynamoDB command


### Setup:
1. Get your Python 2.7 environment created
``` bash
# Create virtual environment (or deal with the pain)
python2 -m virtualenv env
# Activate virtual environment
source env/bin/activate
# Install PIP requirements
pip install -r requirements.txt
```
2. Create a DynamoDB table to collect e-mails
``` bash
aws dynamodb create-table --table-name registrations --attribute-definitions AttributeName=name,AttributeType=S AttributeName=email,AttributeType=S --key-schema AttributeName=email,KeyType=HASH AttributeName=name,KeyType=RANGE --billing-mode PAY_PER_REQUEST
```
3. Deploy the app to your own account
``` bash
zappa deploy dev
```
4. Take the deployment endpoint from Zappa and init first:

   https://WHATEVER_YOUR_ENDPOINT_IS.amazonaws.com/dev/init

5. Once that finishes you'll be redirected to the home page

   _If your CSS doesn't show, it's because FlaskS3 set a metadata tag incorrectly. Change the mime type from binary/octet-stream to text/css in the console (until I can write some code to do it via CLI)._
6. Verify things work by submitting a registration:

   https://WHATEVER_YOUR_ENDPOINT_IS.amazonaws.com/dev/


### Usage:
1. Query DynamoDB for e-mails. This will output as
``` bash
aws dynamodb scan --table-name registrations --query 'Items[*].email' --output text
```
2. Provide the list of e-mails here:

   https://www.qwiklabs.com/my_account/token_allocation_groups


### Clean-up:
1. Delete DynamoDB records
``` bash
# Delete the whole table (cheaper for large datasets; creating new table adds time)
aws dynamodb delete-table --table-name registrations
# OR
# Delete all items from the table (more expensive for large datasets; quicker total time to execute)
aws dynamodb scan --table-name registrations --query 'Items[*]' | jq --compact-output '.[]' | tr '\n' '\0' | xargs -0 -t -I keyItem aws dynamodb delete-item --table-name registrations --key=keyItem
```
2. Undeploy Flask app
``` bash
zappa undeploy dev
```


### Change hero image:
1. Download ImageMagick
  - Mac: `brew install imagemagick`
2. Generate hero images
``` bash
source util/env/bin/activate
python util/generate_heros.py -l /path/to/image.jpg
deactivate
```
  The images will be stored in website/static
3. Update the CSS
``` bash
sed -i 's/chicago/<your_file_name>/' website/static/style.css
# Or on Mac
sed -i '' "s/chicago/<your_file_name/g" website/static/style.css
```
4. Deploy the app
``` bash
cd website
source env/bin/activate
flask run --reload
```
5. Initialize the app (which does upload AND change the style in prod...)

   http://localhost:5000/init
