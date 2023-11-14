# AWS Lambda Function for multi-part image upload/POST to S3

## Deploy

```sh
npm i
sls deploy
```

## Test

```sh
curl \
-X POST \
-H "Content-Type: multipart/form-data" \
-F "image=@test.jpg" \
https://replace_me.execute-api.ap-southeast-2.amazonaws.com/dev/execute

```
