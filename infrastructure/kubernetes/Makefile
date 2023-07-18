.PHONY: deploy
deploy:
	kubectl apply -f deployment.yml
	kubectl apply -f service.yml
	# Creating the ingress immediately with k3s and its traefik ingress doesn't work.
	# Looks like traefik gets into a bad state. Should use `kubectl wait`
	# It works fine with minikube.
	kubectl apply -f ingress.yml

test:
	curl http://localhost:80
