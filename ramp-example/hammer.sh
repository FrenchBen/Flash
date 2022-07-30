#!/usr/bin/env bash

DELAY=1000

echo "Hammering Slow server with ${DELAY}ms delay"
echo "GET http://webapp:3000/delay/${DELAY}" | python ramp-flash.py --prefix direct
echo "----------------------------------------------------"
echo "Hammering Varnish cache server with ${DELAY}ms delay"
echo "GET http://varnish-cache:8080/delay/${DELAY}" | python ramp-flash.py --prefix varnish
echo "----------------------------------------------------"
echo "Hammering Nginx cache server with ${DELAY}ms delay"
echo "GET http://nginx-cache:8081/delay/${DELAY}" | python ramp-flash.py --prefix nginx