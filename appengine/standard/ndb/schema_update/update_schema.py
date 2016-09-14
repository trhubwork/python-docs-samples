import logging
import updated_picture_model
#import models
from google.appengine.ext import deferred
from google.appengine.ext import ndb

BATCH_SIZE = 100  # ideal batch size may vary based on entity size.

class Picture(ndb.Model):
    author = ndb.StringProperty()
    name = ndb.StringProperty(default='')  # Unique name.
    #num_votes = ndb.IntegerProperty(default=0)
    #avg_rating = ndb.FloatProperty(default=0)

def get_current_entities():
    current_entities = list(Picture.query().fetch())
    return current_entities

def add_entity(author_value, name_value):
    new_pic = Picture(author=author_value, name=name_value)
    new_pic.put()
        

def UpdateSchema(cursor=None, num_updated=0):
    Picture = updated_picture_model.Picture()
    query = Picture.query()
    if cursor:
        data, cursor, more = query.fetch_page(BATCH_SIZE, start_cursor=cursor)
    else:
        data, cursor, more = query.fetch_page(BATCH_SIZE)

    to_put = []
    for p in data:
        # In this example, the default values of 0 for num_votes and avg_rating
        # are acceptable, so we don't need this loop.  If we wanted to manually
        # manipulate property values, it might go something like this:
        p.num_votes = 1
        p.avg_rating = 5
        to_put.append(p)

    if to_put:
        ndb.put_multi(to_put)
        #db.put(to_put)
        num_updated += len(to_put)
        logging.debug(
            'Put %d entities to Datastore for a total of %d',
            len(to_put), num_updated)
    if more:
        deferred.defer(
            UpdateSchema, cursor=query.cursor(), num_updated=num_updated)
    else:
        logging.debug(
            'UpdateSchema complete with %d updates!', num_updated)