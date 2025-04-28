# create an item
curl -X POST http://localhost:8000/items/ \
     -H "Content-Type: application/json" \
     -d '{"name":"widget","description":"demo record"}'

# fetch items
curl http://localhost:8000/items/
