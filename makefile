.ONESHELL:
IMAGE=llm-extractor

build:
	docker build . -t $(IMAGE)

run: kill build
	docker run -d \
	-p 8080:8080 \
	$(IMAGE)

kill:
	docker ps -a | grep -w $(IMAGE) | cut -d' ' -f1 | xargs -r docker kill

dev: run
	CONTAINER=$$(docker ps -a | grep -w $(IMAGE) | head -n 1 | cut -d' ' -f1)
	watch "docker logs $$CONTAINER | tail -n 15"

logs:
	CONTAINER=$$(docker ps -a | grep -w $(IMAGE) | head -n 1 | cut -d' ' -f1)
	docker logs $$CONTAINER
