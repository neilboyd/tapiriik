# tapiriik keeps your fitness in sync

## Looking to run tapiriik locally?

Check out the [setup guide on the wiki](https://github.com/cpfair/tapiriik/wiki/Running-tapiriik-locally). It's a bit more than `pip install tapiriik`, but I'm sure you can handle it.

## Docker

The [Dockerfile](Dockerfile) defines all the required services to run in one container.

To run locally with [Docker Compose](https://docs.docker.com/compose/):

- define environment variables in [`docker-compose.yml`](docker-compose.yml)
- run `docker-compose up -d`
- stop `docker-compose down`
- rebuild in case of any changes `docker-compose build`, or `docker-compose up -d --build`

For convenience, everything is in one container.
In order to run at scale,
you should use an external RabbitMQ and MongoDB instance.
That leaves web, sync servers and Redis which can live together and scale together.
[Ideally, Redis should also be an external instance](https://github.com/cpfair/tapiriik/wiki/tapiriik.com-infrastructure#web),
but it's okay to leave it together with the web instances,
or don't use Redis at all (by not defining `REDIS_HOST`).

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
