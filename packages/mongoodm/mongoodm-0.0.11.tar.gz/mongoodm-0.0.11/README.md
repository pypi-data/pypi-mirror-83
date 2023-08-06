# MongoODM

MongoODM is a rediculously simple wrapper around the pymongo and mongomock libraries to provide a way to classify your documents (and test them)

## Example Use
The following is a way you can use the odm and switch dbs on the fly:
```
from mongoodm import MongoODM, Document

uri = 'mongodb://localhost:27017'
db = MongoODM(uri=uri)

uri2 = 'mongodb://localhost:26015'
db2 = MongoODM(uri=uri2)

class User(Document):
    pass

# Get documents from the first db
print(db(User).all())

# Get Documents from the second db
print(db2(User).all())
```

Here's a simple example of creating a class and using it:
```
from mongoodm import MongoODM, Document

class User(Document):
    pass

# This will raise an exception because the db hasn't been initialised
User.find({})

db = MongoODM() # Connects to localhost by default

# This now works
User.find({})
```

If you're used to Django style models here's another way you can use:
```
from mongoodm import MongoODM

db = MongoODM()

class User(db.Document):
    pass

User.find_one({})
```

Have you got flask? You can setup the config values in your app config:
 - `MONGOODM_URI` uri of the mongo instance
 - `MONGOODM_PROVIDER` the provider you want to use (mongomock or pymongo)

```
from flask import Flask
from mongoodm import MongoODM
app = Flask(__name__)
db = MongoODM(app=app)

class User(db.Document):
    pass

@app.route('/')
def hello_world():
    user = User.find_one({'_id': 'me'})
    return 'Hello, %s!' % User.name
```

Want to use a custom collection with your class?

```
from mongoodm import MongoODM

db = MongoODM()

class User(db.Document):
    _collection_name = "people"
    pass
```

Want to use `_id` instead of `id`?
```
from mongoodm import MongoODM

db = MongoODM()

class User(db.Document):
    _restore_id = True
    pass
```

Want your cake and eat it too (have both `id` and `_id` at the same time)?
```
from mongoodm import MongoODM

db = MongoODM()

class User(db.Document):
    _preserve_ids = True
    pass
```