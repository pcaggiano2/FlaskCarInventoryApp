docker build --platform linux/amd64 -t pax7898/car_inventory car_inventory/.
docker build --platform linux/amd64 -t pax7898/vin_decoder vin_decoder/.

docker push pax7898/car_inventory
docker push pax7898/vin_decoder

kubectl apply -f car_inventory/car_inventory.yaml -f vin_decoder/vin_decoder.yaml