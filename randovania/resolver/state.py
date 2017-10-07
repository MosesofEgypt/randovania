import copy

from randovania.resolver.game_description import CurrentResources, Node, ResourceInfo, ResourceNode, ResourceDatabase, \
    PickupDatabase


class State:
    resources: CurrentResources
    node: Node

    def __init__(self, resources: CurrentResources, node: Node):
        self.resources = resources
        self.node = node

    def has_resource(self, resource: ResourceInfo) -> bool:
        return self.resources.get(resource, 0) > 0

    def collect_resource_node(self, node: ResourceNode,
                              resource_database: ResourceDatabase,
                              pickup_database: PickupDatabase) -> "State":
        resource = node.resource

        if self.has_resource(resource):
            raise ValueError(
                "Trying to collect an already collected resource '{}'".format(
                    resource))

        new_resources = copy.copy(self.resources)
        for pickup_resource, quantity in node.resource_gain_on_collect(
                resource_database, pickup_database):
            new_resources[pickup_resource] = new_resources.get(
                pickup_resource, 0)
            new_resources[pickup_resource] += quantity

        return State(new_resources, self.node)

    def act_on_node(self,
                    node: ResourceNode,
                    resource_database: ResourceDatabase,
                    pickup_database: PickupDatabase) -> "State":
        if not isinstance(node, ResourceNode):
            raise ValueError("Can't act on Node of type {}".format(type(node)))

        new_state = self.collect_resource_node(node, resource_database, pickup_database)
        new_state.node = node
        return new_state