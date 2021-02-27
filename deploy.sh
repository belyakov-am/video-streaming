#/bin/sh

terraform init
terraform plan -var "token=$1"
terraform apply -var "token=$1" -auto-approve

terraform output >ips.txt

app_ex=$(cat ips.txt | grep ex_ip_app | grep -E -oh "[0-9]+.[0-9]+.[0-9]+.[0-9]+")

scp -o StrictHostKeyChecking=no -r src/ ubuntu@$app_ex:. 
scp Pipfile* ubuntu@$app_ex:.
scp docker/backend.dockerfile ubuntu@$app_ex:.
ssh ubuntu@$app_ex "cat *dockerfile > Dockerfile"
ssh ubuntu@$app_ex "mv src/run.sh ."
ssh ubuntu@$app_ex "chmod +x run.sh"
ssh -t ubuntu@$app_ex "sudo ./run.sh"

rm ips.txt

