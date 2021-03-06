# Elasticsearch template. To be used only once.
curl -XPOST  'atlas-kibana.mwt2.org:9200/_template/xcache' -d '{
    "order": 0,
    "index_patterns": "xcache*",
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 1
    },    
    "aliases": {
      "xcache": {}
    },
    "mappings": {
      "docs": {
        "properties": {
          "site": {
            "type": "keyword"
          },
          "sender": {
            "type": "keyword"
          },
          "type": {
            "type": "keyword"
          },
          "host": {
            "type": "keyword"
          },
          "file": {
            "type": "keyword"
          },
          "size": {
            "type": "long"
          },
          "created_at": {
            "type": "date"
          },
          "attached_at": {
            "type": "date"
          },
          "detached_at": {
            "type": "date"
          },
          "bytes_disk": {
            "type": "long"
          },
          "bytes_ram": {
            "type": "long"
          },
          "bytes_missed": {
            "type": "long"
          }
        }
      }
    }
  }
}'
