RELEASE=dev



vm:
	ssh -i ~/.ssh/google_compute_engine -o UserKnownHostsFile=/dev/null -o CheckHostIP=no -o StrictHostKeyChecking=no ${GC_USERNAME}@${GC_IP}

env-active:
	source ${PWD}/venv/bin/activate

copy_to_vm:
	scp -i ~/.ssh/google_compute_engine .dockerignore ${GC_USERNAME}@${GC_IP}:factsheets/.dockerignore
	scp -i ~/.ssh/google_compute_engine app.py ${GC_USERNAME}@${GC_IP}:factsheets/app.py
	scp -i ~/.ssh/google_compute_engine Dockerfile ${GC_USERNAME}@${GC_IP}:factsheets/Dockerfile
	scp -i ~/.ssh/google_compute_engine Makefile ${GC_USERNAME}@${GC_IP}:factsheets/Makefile
	scp -i ~/.ssh/google_compute_engine setup.py ${GC_USERNAME}@${GC_IP}:factsheets/setup.py

	scp -i ~/.ssh/google_compute_engine -r factsheets ${GC_USERNAME}@${GC_IP}:factsheets/factsheets
	scp -i ~/.ssh/google_compute_engine -r static/img ${GC_USERNAME}@${GC_IP}:factsheets/staticimg/
	scp -i ~/.ssh/google_compute_engine -r static/js ${GC_USERNAME}@${GC_IP}:factsheets/static/js
	scp -i ~/.ssh/google_compute_engine static/package.json ${GC_USERNAME}@${GC_IP}:factsheets/static/package.json
	scp -i ~/.ssh/google_compute_engine static/webpack.config.js ${GC_USERNAME}@${GC_IP}:factsheets/static/webpack.config.js
	scp -i ~/.ssh/google_compute_engine -r templates ${GC_USERNAME}@${GC_IP}:factsheets/templates

mongo-spin:
	docker run \
		-d \
		-p 27017:27017 \
		-v ${FS_MONGO_PATH}:/data/db \
		--network factsheets \
		--name factsheets-mongo \
		mongo:latest

docker-build-image:
	docker build . --tag factsheets:${RELEASE}

docker-rebuild-image:
	docker run -itd --name factsheets-$(RELEASE) factsheets:$(RELEASE)

	# docker exec factsheets bash -c 'rm -rf factsheets/static'
	#docker cp static factsheets:factsheets/static

	docker exec factsheets-$(RELEASE) bash -c 'rm -rf factsheets/templates'
	docker cp templates factsheets-$(RELEASE):factsheets/templates

	docker exec factsheets-$(RELEASE) bash -c 'rm -rf factsheets/factsheets'
	docker cp factsheets factsheets-$(RELEASE):factsheets/factsheets

	docker cp app.py factsheets-$(RELEASE):factsheets/app.py

	# docker exec factsheets bash -c 'npm run --prefix /factsheets/static build'

	docker commit factsheets-$(RELEASE) factsheets:$(RELEASE)
	docker rm -f factsheets-$(RELEASE)

docker-run-service:
	docker run \
		-p 5000:5000 \
		-e "FS_MONGO_HOST=factsheets-mongo" \
		-e "FS_MONGO_PORT=${FS_MONGO_PORT}" \
		--network factsheets \
		-d \
		factsheets:$(RELEASE) python /factsheets/app.py

docker-run-service-attached:
	docker run \
		-it \
		-p 5000:5000 \
		-e "FS_MONGO_HOST=factsheets-mongo" \
		-e "FS_MONGO_PORT=${FS_MONGO_PORT}" \
		--network factsheets \
		--name factsheets-$(RELEASE) \
		factsheets:$(RELEASE) /bin/bash

docker-rc:
	docker rm -f factsheets-$(RELEASE)

docker-log:
	docker logs factsheets-$(RELEASE) --follow