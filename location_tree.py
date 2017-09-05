import sqlalchemy
import tree
import pandas as pd


def get_tree(location_set_version_id):
    """ Constructs and returns a tree representation of the location
    hierarchy specified by location_set_version_id """
    mysql_server = (
            'mysql+pymysql://dbview:E3QNSLvQTRJm@modeling-cod-db.ihme.washington.edu:3306')
    e = sqlalchemy.create_engine(mysql_server)#failing here
    c = e.connect()


    locsflat = pd.read_sql("""
        SELECT location_id, parent_id, is_estimate, super_region_id, location_hierarchy_history.location_name_short, location_hierarchy_history.map_id, location_hierarchy_history.location_type, location_hierarchy_history.super_region_id
        FROM shared.location_hierarchy_history
        JOIN shared.location USING(location_id)
        JOIN shared.location_type ON location_hierarchy_history.location_type_id=location_type.location_type_id
        WHERE location_set_version_id=%s""" % location_set_version_id, c.connection)

    root = locsflat[locsflat.location_id==166]
    print("ROOT is: {root}".format(root=root.location_name_short))
    root_node = tree.Node(root.location_id, root.to_dict('records')[0], None)
    print("Root info is: {info}".format(info=root_node.info['location_name_short']))
    #root_node = tree.Node(166, root.to_dict('records')[0], [1])

    #Construct all nodes THAT ARE CHILDREN OF SUB-SAHARAN AFRICA
    nodes = {root_node.id: root_node}
    for i, row in locsflat[locsflat.location_id!=root_node.id].iterrows():
        node = tree.Node(row.location_id, row.to_dict(), None)
        #WALK THE TREE TO SEE IF IT IS A CHILD
        if node.info['super_region_id'] == 166:
            nodes[node.id] = node

            print("A child is {called} {name}".format(called=node.info['location_id'],name=node.info['location_name_short']))


    #Assign parents
    for node_id,node in nodes.iteritems():
        if node_id!=root_node.info['location_id']:#node.info['parent_id']:
            node.parent = nodes[node.info['parent_id']]
            node.parent.add_child(node)

    #import pdb
    #pdb.set_trace()
    location_tree = tree.Tree(root_node)

    for node in location_tree.nodes:
        if node.info['location_type'] in ['superregion','global','region']:
            #print("PLACE {name}".format(name=node.info['location_name_short']))
            #print("SUPERREGION {child}".format(child=node.info['super_region_id']))
            name = node.info['location_name_short']
            name = name.replace(" ","_")
            name = name.replace(",","")
            name = name.replace("-","_")
            name = name.lower()
        elif node.info['map_id'] is None:
            name = str(node.info['location_id'])
        else:
            name = node.info['map_id'].lower()
        node.info['dismod_name'] = name #rename this from 'dismod_name'

    #for node in location_tree.nodes:
    #    if node.info[super_region_id] == 166.0:
    #        print("MEMBER {location}".format(location=node.info['location_name_short']))

    #Assign dismod levels
    #dont need dismod
    for node in location_tree.level_n_descendants(0):
        print("New node: {id}".format(id=node.info['location_name_short']))
        node.info['level'] = 'world'
    for node in location_tree.level_n_descendants(1):
        print("New node: {id}".format(id=node.info['location_name_short']))
        node.info['level'] = 'super'
    for node in location_tree.level_n_descendants(2):
        print("New node: {id}".format(id=node.info['location_name_short']))
        node.info['level'] = 'region'
    for node in location_tree.level_n_descendants(3):
        print("New node: {id}".format(id=node.info['location_name_short']))
        node.info['level'] = 'subreg'
    for lvl in range(4,8):
        for node in location_tree.level_n_descendants(lvl):
            #print("New node: {id}".format(id=node.info))
            node.info['level'] = 'atom'

    return location_tree

new_tree = get_tree(#scraped)




