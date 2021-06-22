#!/bin/bash

TRACE_ID=$(hexdump -n 16 -e '4/4 "%x" 1 "\n"' /dev/random)
SPAN_ID=$(hexdump -n 8 -e '4/4 "%x" 1 "\n"' /dev/random)

BEGIN_TIME=$(date +%s000000000)
curl -H "traceparent: 00-${TRACE_ID}-${SPAN_ID}-01" http://localhost:5001/alpha/foo
sleep 1
END_TIME=$(date +%s000000000)

curl  http://localhost:55681/v1/traces -H 'Content-Type: application/json' -d @- <<EOF
{
	  "resource_spans": [
		{
		  "resource": {
			"attributes": [
			  {
				"key": "service.name",
				"value": { "stringValue": "iOS Agent" }
			  }
			]
		  },
		  "instrumentation_library_spans": [
			{
			  "spans": [
				{
				  "trace_id": "${TRACE_ID}",
				  "span_id": "${SPAN_ID}",
				  "name": "mobile-network-request",
				  "start_time_unix_nano": ${BEGIN_TIME},
				  "end_time_unix_nano": ${END_TIME},
				  "attributes": [
					{
					  "key": "attr1",
					  "value": { "intValue": 55 }
					}
				  ]
				}
			  ]
			}
		  ]
		}
	  ]
	}
EOF
echo
echo check http://localhost:9411/zipkin/traces/${TRACE_ID}
