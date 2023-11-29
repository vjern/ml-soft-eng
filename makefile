.ONESHELL:
IMAGE=llm-extractor

build:
	docker build . -t $(IMAGE)

run: build
	docker run -d \
	$(IMAGE)

dev: run
	CONTAINER=$$(docker ps -a | grep -w $(IMAGE) | head -n 1 | cut -d' ' -f1)
	watch "docker logs $$CONTAINER | tail -n 15"

logs:
	CONTAINER=$$(docker ps -a | grep -w $(IMAGE) | head -n 1 | cut -d' ' -f1)
	docker logs $$CONTAINER
