from indalsig.domain import Way, Node, WayNode, Address, Postcode


class WayDAO:

    def __init__(self, session):
        self.session = session

    def get(self, idx):
        return self.session.query(Way).get(idx)

    def save(self, item):

        self.session.add(item)

    def search_by_openstreetmap_id(self, openstreetmap_id):
        return self.session.query(Way)\
            .filter(Way.openstreetmap_id == openstreetmap_id)\
            .first()


class NodeDAO:

    def __init__(self, session):
        self.session = session

    def get(self, idx):
        return self.session.query(Node).get(idx)

    def save(self, item):
        self.session.add(item)

    def search_by_openstreetmap_id(self, openstreetmap_id):
        return self.session.query(Node)\
            .filter(Node.openstreetmap_id == openstreetmap_id)\
            .first()


class WayNodeDAO:

    def __init__(self, session):
        self.session = session

    def get(self, idx):
        return self.session.query(WayNode).get(idx)

    def save(self, item):
        self.session.add(item)

    def search_by_way_and_node(self, way_id, node_id):
        return self.session.query(WayNode)\
            .filter(WayNode.way_id == way_id
                    and WayNode.node_id == node_id)\
            .first()


class AddressDAO:

    def __init__(self, session):
        self.session = session

    def get(self, idx):
        return self.session.query(Address).get(idx)

    def save(self, item):
        self.session.add(item)


class PostcodeDAO:

    def __init__(self, session):
        self.session = session

    def get(self, idx):
        return self.session.query(Address).get(idx)

    def save(self, item):
        self.session.add(item)

    def search_by_postcode(self, postcode):
        return self.session.query(Postcode).filter(Postcode.postcode == postcode).first()

