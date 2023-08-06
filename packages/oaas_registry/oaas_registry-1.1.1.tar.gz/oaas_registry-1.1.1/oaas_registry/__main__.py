# we import these two, to expose the oaas-registry service
import logging
import sys

import oaas
from oaas_grpc.client.client import OaasGrpcClient
from oaas_grpc.server import OaasGrpcServer
from oaas_registry.oaas_grpc_registry import noop

noop()  # we have this function call so the optimize
# import keeps the registry definition

LOG = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stderr)

    oaas.register_server_provider(OaasGrpcServer())
    oaas.register_client_provider(OaasGrpcClient())

    oaas.serve()
    LOG.info("OaaS Registry listening on 8999")
    oaas.join()


if __name__ == "__main__":
    main()
