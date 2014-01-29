nlevel
======

N-level hierarchical nodes built on redis

setup & running
---------------

Requires a local [redis](http://redis.io/download) server.  Should probably also be installed in a virtualenv.

    $ git clone git@github.com:benwilber/nlevel.git
    $ cd nlevel
    $ mkvirtualenv nlevel
    $ pip install -r requirements.txt
    $ python restapi.py
    
rest api
--------

__create a root node__
    
    POST /api/v1/nodes school=The+Hogwarts+School+of+Witchcraft+and+Wizardry
    {
      "key": "n:1",
      "info": {
        "school": "The Hogwarts School of Witchcraft and Wizardry", 
      }
    }

__list root nodes__

    GET /api/v1/nodes
    [
      {
        "key": "n:1"
        "info": {
          "school": "The Hogwarts School of Witchcraft and Wizardry"
        }
      }
    ]
    
__get a node__

    GET /api/v1/nodes/n:1
    {
      "key": "n:1"
      "info": {
        "school": "The Hogwarts School of Witchcraft and Wizardry"
      }
    }

__create a child node__

    POST /api/v1/nodes/n:1/nodes name=Harry+Potter
    {
      "key": "n:2",
      "parent": "n:1",
      "info": {
        "name": "Harry Potter"
      }
    }

__list child nodes__

    GET /api/v1/nodes/n:1/nodes
    [
      {
        "key": "n:2",
        "parent": "n:1",
        "info": {
          "name": "Harry Potter"
        }
      }
    ]
