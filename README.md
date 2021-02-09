# tapiriik keeps your fitness in sync

## This fork

This repo is forked from https://github.com/cpfair/tapiriik.  
It has been updated to reflect changes in the dependencies,
and it's running on Kubernetes on [siiink.com](https://www.siiink.com).

## Looking to run tapiriik locally?

Check out the [setup guide on the wiki](https://github.com/cpfair/tapiriik/wiki/Running-tapiriik-locally). It's a bit more than `pip install tapiriik`, but I'm sure you can handle it.

## Docker

The [Dockerfile](Dockerfile) defines all the required services to run in one container.

To run locally with [Docker Compose](https://docs.docker.com/compose/):

- define environment variables in [`docker-compose.yml`](docker-compose.yml)
- run `docker-compose up -d`
- stop `docker-compose down`
- rebuild in case of any changes `docker-compose build`, or `docker-compose up -d --build`

To run on Kubernetes,
eg [AKS](https://docs.microsoft.com/en-us/azure/aks/):
- edit [`kubernetes-secrets.yml`](kubernetes-secrets.yml) (or a copy of it)
- `kubectl apply -f kubernetes-secrets.yml --namespace tapiriik`
- `kubectl apply -f kubernetes.yml --namespace tapiriik`
- add [TLS ingress](https://docs.microsoft.com/en-us/azure/aks/ingress-tls)

## Want to help with development?

**Great!** If you're looking for a quick primer on how tapiriik functions under the hood, head on over to the [technical introduction wiki article](https://github.com/cpfair/tapiriik/wiki/tapiriik-internals). Once you're ready, send in a pull request and I'll work with you to get it merged.

## Just want to synchronize your fitness activities?

Visit [siiink.com](https://www.siiink.com) - everything's already set up for you.

## Licensing

tapiriik is an Apache 2.0 Licensed open-source project. If you'd like to use the tapiriik name or logo, please drop me a line.
