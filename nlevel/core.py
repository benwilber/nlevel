from functools import partial

def next_id(r):
    return r.incr("nlevel_ids")


def make_key(*parts):
    return ":".join(map(str, parts))

make_node_key = partial(make_key, "n")
make_meta_key = partial(make_key, "m")
make_index_key = partial(make_key, "i")

def list_to_pairs(flat_list):
    return zip(flat_list[::2], flat_list[1::2])


def render(key, info, meta):
    m = {'key': key, 'info': info}
    if 'p' in meta:
        m['parent'] = meta['p']
    return m

def node(r, info, parent=None):
    id = next_id(r)
    node_key = make_node_key(id)
    meta_key = make_meta_key(node_key)

    if parent:
        index_key = make_index_key(parent)
    else:
        index_key = make_index_key("nlevel_roots")

    with r.pipeline() as pipe:
        pipe.hmset(node_key, info)
        pipe.zadd(index_key, node_key, float(id))
        if parent:
            pipe.hset(meta_key, 'p', parent)
        pipe.execute()
    return node_key


def info(r, node_key):
    meta_key = make_meta_key(node_key)

    with r.pipeline() as pipe:
        pipe.hgetall(node_key)
        pipe.hgetall(meta_key)
        info, meta = pipe.execute()
        return render(node_key, info, meta)


def nodes(r, key):
    index_key = make_index_key(key)

    node_keys = r.zrange(index_key, 0, -1)
    with r.pipeline() as pipe:
        for node_key in node_keys:
            pipe.hgetall(node_key)
            pipe.hgetall(make_meta_key(node_key))
        pairs = list_to_pairs(pipe.execute())

    args = [[key] + list(pairs) for key, pairs in zip(node_keys, pairs)]
    return map(lambda x: render(*x), args)


def roots(r):
    return nodes(r, "nlevel_roots")



if __name__ == '__main__':
    import redis
    r = redis.Redis()
    key = node(r, {"name": 1})
    for i in range(1, 20):
        k = node(r, {"name": i}, parent=key)
        print nodes(r, key)
        key = k

    print roots(r)









