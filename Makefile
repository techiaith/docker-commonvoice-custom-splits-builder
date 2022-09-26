default: build

config:
	mkdir -p ${PWD}/data/	


build: config
	if [ ! -d "CorporaCreator" ]; then \
	    git clone https://github.com/common-voice/CorporaCreator.git; \
	fi
	docker build --rm -t techiaith/commonvoice-custom-splits-builder .


run: config
	docker run --name commonvoice-custom-splits-builder \
		--restart=always \
		-it \
		-v ${PWD}/data/:/data \
		-v ${PWD}/python/:/custom-commonvoice \
		techiaith/commonvoice-custom-splits-builder bash


stop:
	-docker stop commonvoice-custom-splits-builder
	-docker rm commonvoice-custom-splits-builder


clean: stop
	-docker rmi techiaith/commonvoice-custom-splits-builder


purge: clean
	sudo rm -rf data
