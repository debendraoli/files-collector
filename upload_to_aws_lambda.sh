printf "Zipping files using 'zip' with compresson level 9\n"
sleep 1
zip -r9u function.zip .
printf "Zipped.\n"
sleep 1
printf "Uploading compressed file 'function.zip' to aws lambda.\n"
aws lambda update-function-code \
    --function-name crawler \
    --zip-file fileb://function.zip
printf "Uploaded compressed file 'function.zip' to aws lambda.\n"
sleep 1
printf "Setting up environment variable for lambda function.\n"
aws lambda update-function-configuration \
    --function-name crawler \
    --environment Variables="
    {
    DB_HOST='localhost',
    DB_NAME='test',
    DB_USER='root',
    DB_PASSWORD='',
    AWS_SQS_NAME='files'
    }"