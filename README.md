# tapiriik keeps your fitness in sync

## Looking to run tapiriik locally?

Check out the [setup guide on the wiki](https://github.com/cpfair/tapiriik/wiki/Running-tapiriik-locally). It's a bit more than `pip install tapiriik`, but I'm sure you can handle it.

## Docker

The [Dockerfile](Dockerfile) defines all the required services to run in one container.

To run locally with [Docker Compose](https://docs.docker.com/compose/):

- define environment variables in [`docker-compose.yml`](docker-compose.yml)
- run `docker-compose up -d`
- stop `docker-compose down`
- rebuild in case of any changes `docker-compose build` [`--no-cache`]

To run on a hosted service such as
[Web App for Containers](https://azure.microsoft.com/en-us/services/app-service/containers/)
or
[Azure Container Instances](https://azure.microsoft.com/en-us/services/container-instances/)
define the environment variables on the server.
NB: you'll also need to define [`WEBSITES_PORT=8000`](https://docs.microsoft.com/en-us/azure/app-service/configure-custom-container?pivots=container-linux#configure-port-number).

For convenience, everything is in one container.
In order to run at scale,
you should use an external RabbitMQ and MongoDB instance.
That leaves web, sync servers and Redis which can live together and scale together.
[Ideally, Redis should also be an external instance](https://github.com/cpfair/tapiriik/wiki/tapiriik.com-infrastructure#web),
but it's okay to leave it together with the web instances,
or don't use Redis at all (by not defining `REDIS_HOST`).

## Want to help with development?

**Great!** If you're looking for a quick primer on how tapiriik functions under the hood, head on over to the [technical introduction wiki article](https://github.com/cpfair/tapiriik/wiki/tapiriik-internals). Once you're ready, send in a pull request and I'll work with you to get it merged.

## Just want to synchronize your fitness activities?

Visit [tapiriik.com](https://tapiriik.com) - everything's already set up for you.

## Licensing

tapiriik is an Apache 2.0 Licensed open-source project. If you'd like to use the tapiriik name or logo, please drop me a line.
