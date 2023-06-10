# databricks-proxy
With Informatca BDM and other older databricks compatible tools, those tools don't always keep up with API changes and enhancement. This cluster proxy will help take cluster API requests, modify them, then forward them to the `DATABRICKS_HOST` api endpoint.

cluster_proxy.py is a simple Flask app to create a simple localhost only cluster api proxy endpoint.
Use this proxy to modify requests being made to `DATABRICKS_HOST` api endpoint.

Documentation inside cluster_proxy.py


## Testing
In one shell, run the proxy service
```sh
export DATABRICKS_HOST=https://myorg-myworkspace.cloud.databricks.com python cluster_proxy.py
```
Should produce:
```
 * Serving Flask app 'cluster_proxy'
 * Debug mode: off
[2023-06-10 17:47:06,728] INFO in _internal: WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:8080
[2023-06-10 17:47:06,728] INFO in _internal: Press CTRL+C to quit
```
In separate shell, edit `cluster.json` and add your cluster config (hint, copy paste JSON from cluster UI -> JSON (upper right corner). Save the JSON as your cluster.json file. This is your testing template.
Then run:
```sh
bash ./cluster-create.sh
```
Should produce something like:
```
{"cluster_id":"9999-999999-w1srxxdm"}%
```
