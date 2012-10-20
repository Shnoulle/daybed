import json
from cornice import Service
from pyramid.exceptions import NotFound

from daybed.validators import schema_validator

data = Service(name='data',
               path='/data/{model_name}',
               description='Model data',
               renderer="jsonp")


@data.get()
def get(request):
    """Retrieves all model records."""
    model_name = request.matchdict['model_name']
    # Check that model is defined
    exists = request.db.get_definition(model_name)
    if not exists:
        raise NotFound("Unknown model %s" % model_name)
    # Return array of records
    results = request.db.get_data(model_name)
    # TODO: Maybe we need to keep ids secret for editing
    data = []
    for result in results:
        result.value['id'] = result.id
        data.append(result.value)
    return {'data': data}


@data.post(validators=schema_validator)
def post(request):
    """Saves a model record.

    Posted data fields will be matched against their related model
    definition.

    """
    model_name = request.matchdict['model_name']
    data_doc = {
        'type': 'data',
        'model_name': model_name,
        'data': json.loads(request.body)
    }
    _id, rev = request.db.save(data_doc)
    return {'id': _id}