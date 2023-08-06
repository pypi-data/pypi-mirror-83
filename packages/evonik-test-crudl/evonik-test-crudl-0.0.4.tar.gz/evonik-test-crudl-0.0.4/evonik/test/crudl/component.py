import pytest


class Component:
    """CRUDL component that can (at least) be created and deleted.

    A Component is specified mainly by an Endpoints object. This
    must contain the different endpoints for, e.g., creating and
    deleting an entry but none are enforced.
    
    Furthermore, it holds a list of referenced components, e.g.,
    components that must exist and are referenced by an id.
    An example would be a user Component which references a department
    Component which references a company component. When creating
    a user, we must specify the referenced department, e.g., via a
    department_id, which identifies an existing department.

    Example:
        company = Component("Company", company_endpoints)
        user = Component("User", user_endpoints, [company])
    
    Args:
        name (:obj:`str`):
            Name of the component.
        endpoints (:obj:`Endpoints`):
            Endpoints for this component.
        references (:obj:`list` of :obj:`str`):
            List of referenced components.
    """
    def __init__(self, name, endpoints, references=None):
        if not all([hasattr(endpoints, k) for k in ["create", "delete"]]):
            raise ValueError("Component must have create and delete endpoints. "
                             + "Only has: {}".format(list(endpoints.__dict__.keys())))
        self.name = name
        self.endpoints = endpoints
        self.references = references if references else {}
    
    def __str__(self):
        return "'{}' component".format(self.name)

    def valids(self,
               endpoint=None,
               count=1,
               exhaustive=False,
               add_references=True,
               one_reference_each=True,
               values=None,
               **kwargs
               ):
        endpoint = endpoint if endpoint else self.endpoints.create
        values = values if values else {}

        valids = []
        refs = {}
        for valid in endpoint.dummy.valids(count=count, exhaustive=exhaustive, **kwargs):
            valid = {**valid, **values}
            if add_references:
                for k, ref_comp in self.references.items():
                    if k in endpoint.dependencies and k not in valid:
                        if one_reference_each or k not in refs:
                            spec = ref_comp.valids()[0]
                            refs[k] = ref_comp.endpoints.create.call(spec)
                        valid[k] = refs[k]["id"]
            valids.append(valid)
        return valids

    def invalids(self,
                 endpoint=None,
                 count=1,
                 exhaustive=True,
                 add_references=True,
                 one_reference_each=False,
                 values=None,
                 **kwargs
                 ):
        endpoint = endpoint if endpoint else self.endpoints.create
        values = values if values else {}

        invalids = []
        refs = {}
        for invalid in endpoint.dummy.invalids(count=count, exhaustive=exhaustive, **kwargs):
            if isinstance(invalid, tuple):
                invalid, reason = invalid
            else:
                reason = None
            invalid = {**invalid, **values}
            if add_references:
                for k, ref_comp in self.references.items():
                    if k in endpoint.dependencies and k not in invalid:
                        if one_reference_each or k not in refs:
                            spec = ref_comp.valids()[0]
                            refs[k] = ref_comp.endpoints.create.call(spec)
                        invalid[k] = refs[k]["id"]
            if reason is None:
                invalids.append(invalid)
            else:
                invalids.append((invalid, reason))
        return invalids

    def create(self, spec=None, **kwargs):
        endpoint = self.endpoints.create
        if spec is None:
            spec = self.valids(endpoint=endpoint, **kwargs)[0]
        return endpoint.call(spec)

    def read(self, data):
        return self.endpoints.read.call(data)

    def update(self, data, spec=None, **kwargs):
        endpoint = self.endpoints.update
        if spec is None:
            spec = self.valids(endpoint=endpoint ** kwargs)[0]
        return endpoint.call(data, spec)

    def delete(self, data):
        return self.endpoints.delete.call(data)

    def list(self, limit=None, offset=None):
        limit = limit if limit else 10
        offset = offset if offset else 0
        return self.endpoints.list.call(limit, offset)
