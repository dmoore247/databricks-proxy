#
## Test Create Cluster Proxy
#
# -v for debug
#

curl --netrc \
-X POST \
-H "Content-Type: application/json" \
-d @cluster.json \
http://localhost:8080/api/2.0/clusters/create


