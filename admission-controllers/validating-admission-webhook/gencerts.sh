#!/bin/bash

mkdir -p $HOME/ssl

cat << EOF > $HOME/ssl/req.cnf
[req]
req_extensions = v3_req
distinguished_name = req_distinguished_name

[req_distinguished_name]

[ v3_req ]
keyUsage = nonRepudiation, digitalSignature, keyEncipherment
subjectAltName = @alt_names

[alt_names]
DNS.1 = validating-webhook-demo.default.svc
EOF

openssl genrsa -out $HOME/ssl/ca.key 2048
openssl req -x509 -sha256 -new -nodes -key $HOME/ssl/ca.key -days 3650 -subj "/CN=demo-self-ca,/O=devops" -out $HOME/ssl/ca.crt

openssl genrsa -out $HOME/ssl/server.key 2048
openssl req -new -key $HOME/ssl/server.key -out $HOME/ssl/server.csr -subj "/CN=validating-webhook-demo.default.svc/O=kubernetes" -config $HOME/ssl/req.cnf
openssl x509 -req -in $HOME/ssl/server.csr -CA $HOME/ssl/ca.crt -CAkey $HOME/ssl/ca.key -CAcreateserial -out $HOME/ssl/server.crt -days 1000 -extensions v3_req -extfile $HOME/ssl/req.cnf