#!/bin/sh
# insert url
curl --dump-header - -H "Content-Type: application/json" -X POST --data '{"long_url": "http://hakta.com"}' "http://localhost:8000/api/v1/url/?username=test&api_key=1879ed2609d67897fc9ed1ec0b7323a5e98842b9"

# wait 5 seconds
sleep 5

# query url
curl --dump-header - -H "Content-Type: application/json" "http://localhost:8000/api/v1/url/1/?username=test&api_key=1879ed2609d67897fc9ed1ec0b7323a5e98842b9"
