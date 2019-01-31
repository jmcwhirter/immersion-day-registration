

``` bash
aws dynamodb create-table --table-name registrations --attribute-definitions AttributeName=name,AttributeType=S AttributeName=email,AttributeType=S --key-schema AttributeName=email,KeyType=HASH AttributeName=name,KeyType=RANGE --billing-mode PAY_PER_REQUEST
```

``` bash
aws dynamodb scan --table-name registrations --query 'Items[*].email' --output text
```
