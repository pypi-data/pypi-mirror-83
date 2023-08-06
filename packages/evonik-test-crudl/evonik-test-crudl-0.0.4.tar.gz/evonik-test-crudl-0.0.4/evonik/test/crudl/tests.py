import pytest
from .instance import Instance

def _validate_dict(spec, res):
    for k,v in spec.items():
        assert res[k] == v, "{}: {} != {}".format(k, res[k], v)


def create_valids(component, validate_result=_validate_dict, **kwargs):
    """Test the create endpoint with valid data.

    A list of valid specs for the create endpoint is generated.
    Then, the endpoint is called with each spec and the result validated
    using the `validate_result` function.

    Args:
        component (:obj:`Component`)
            The component whose create endpoint to test.
        validate_result (func, optional): Function to validate
            the result of the create call. It must have the
            following signature: `validate_result(spec, res)`
            Here, `spec` is the spec passed to the create endpoint
            and `res` is the result returned by calling it. In the
            function, use assert to validate the results so that
            invalid data leads to an assertion error.
            If it is unspecified, `spec` and `res` are assumed to be
            of type dict and all `k`,`v` in `spec` must be the
            same for `res`.
        kwargs
            Additional keyword args are passed to the valids method
            of the component when creating the valid test specs.

    Returns:
        list: List of the valid specs generated and tested.
    """
    valids = component.valids(**{
        **kwargs,
        "endpoint": component.endpoints.create,
    })
    print("TEST CREATE VALIDS:", len(valids))
    for valid in valids:
        print("VALID CREATE SPEC:", valid)
        data = component.endpoints.create.call(valid)
        assert data is not None, "result from create endpoint should not be None"
        validate_result(valid, data)
    return valids


def create_invalids(component, exception_type=Exception, **kwargs):
    """Test the create endpoint with invalid data.

    A list of invalid specs for the create endpoint is generated.
    Then, the endpoint is called with each spec and asserted that
    the call raises an exception of the specified type.

    Args:
        component (:obj:`Component`)
            The component whose create endpoint to test.
        exception_type (:obj:`Exception`, optional): The exception
            type that is expected to be thrown when calling the
            endpoint with the invalid data. By default, Exception
            is used.
        kwargs
            Additional keyword args are passed to the invalids method
            of the component when creating the invalid test specs.

    Returns:
        list: List of the invalid specs generated and tested.
    """
    invalids = component.invalids(**{
        **kwargs,
        "endpoint": component.endpoints.create,
        "reason": True,
    })
    print("TEST CREATE INVALIDS:", len(invalids))
    for invalid,reason in invalids:
        print("INVALID CREATE SPEC:", invalid)
        print("             REASON:", reason)
        with pytest.raises(exception_type):
            component.endpoints.create.call(invalid)
    return invalids


def read_valids(component, validate_result=_validate_dict, **kwargs):
    valids = component.valids(**{
        "endpoint": component.endpoints.create,
        **kwargs
    })
    print("TEST READ VALIDS:", len(valids))
    for valid in valids:
        print("VALID CREATE SPEC:", valid)
        data = component.endpoints.create.call(valid)
        res = component.endpoints.read.call(data)
        assert res, "result of read endpoint None for {}".format(data)
        validate_result(data, res)
    return valids


def read_invalids(component, invalids, **kwargs):
    print("TEST READ INVALIDS:", len(invalids))
    for invalid in invalids:
        print("INVALID READ SPEC:", invalid)
        with pytest.raises(Exception) as e:
            component.endpoints.read.call(invalid)
    return invalids


def update_valids(component, validate_result=_validate_dict, **kwargs):
    """Test the update endpoint with valid data.

    Lists of valid specs for the create and update endpoints are generated.
    For each spec pair, an entry is created using the valid create spec
    and the update endpoint is called with the valid update spec.
    The result is then validated validated using the `validate_result`
    function.

    Args:
        component (:obj:`Component`)
            The component whose create endpoint to test.
        validate_result (func, optional): Function to validate
            the result of the update call. It must have the
            following signature: `validate_result(spec, res)`
            Here, `spec` is the spec passed to the update endpoint
            and `res` is the result returned by calling it. In the
            function, use assert to validate the results so that
            invalid data leads to an assertion error.
            If it is unspecified, `spec` and `res` are assumed to be
            of type dict and all `k`,`v` in `spec` are asserted to
            be the same for `res`.
        kwargs
            Additional keyword args are passed to the valids method
            of the component when creating the valid test specs.

    Returns:
        list: List of the valid specs generated and tested.
    """
    update_valids = component.valids(**{
        **kwargs,
        "endpoint": component.endpoints.update,
    })
    create_valids = component.valids(**{
        "count": len(update_valids),
        "endpoint": component.endpoints.create,
    })
    print("TEST UPDATE VALIDS:", len(update_valids))
    for create_valid,update_valid in zip(create_valids,update_valids):
        print("VALID CREATE SPEC:", create_valid)
        print("VALID UPDATE SPEC:", update_valid)
        data = component.endpoints.create.call(create_valid)
        data_updated = component.endpoints.update.call(data, update_valid)
        assert data_updated, "result of update endpoint None for {} / {}".format(data, update_valid)
        validate_result(update_valid, data_updated)
        data_read = component.endpoints.read.call(data)
        validate_result(update_valid, data_read)
    return update_valids


def update_invalids(component, exception_type=Exception, **kwargs):
    """Test the update endpoint with invalid data.

    Lists of valid specs for the create and update endpoints are generated.
    For each spec pair, an entry is created using the valid create spec
    and the update endpoint is called with the invalid update spec.
    It is asserted that the call raises an exception of the specified type.

    Args:
        component (:obj:`Component`)
            The component whose create endpoint to test.
        exception_type (:obj:`Exception`, optional): The exception
            type that is expected to be thrown when calling the
            endpoint with the invalid data. By default, Exception
            is used.
        kwargs
            Additional keyword args are passed to the invalids method
            of the component when creating the invalid test specs.

    Returns:
        list: List of the invalid specs generated and tested.
    """
    update_invalids = component.invalids(**{
        **kwargs,
        "endpoint": component.endpoints.update,
        "reason": True,
    })
    create_valids = component.valids(**{
        "endpoint": component.endpoints.create,
        "count": len(update_invalids)
    })
    print("TEST UPDATE INVALIDS:", len(update_invalids))
    for create_valid, update_invalid in zip(create_valids, update_invalids):
        update_invalid, reason = update_invalid
        print("  VALID CREATE SPEC:", create_valid)
        print("INVALID UPDATE SPEC:", update_invalid)
        print("             REASON:", reason)
        data = component.endpoints.create.call(create_valid)
        with pytest.raises(exception_type):
            component.endpoints.update.call(data, update_invalid)
    return update_invalids


def delete_valids(component, validate_result=_validate_dict, exception_type=Exception, **kwargs):
    """Test the delete endpoint with valid data.

    A list of valid specs for the create endpoint is generated.
    Then, each valid spec is passed to the create endpoint of the
    component. Then, the result of that call is passed to the delete
    endpoint. Its result is then validated validated using the
    `validate_result` function. Finally, the delete endpoint is
    called a second time ith the same data and it is asserted that
    an exception of specified type is raised.

    Args:
        component (:obj:`Component`)
            The component whose create endpoint to test.
        validate_result (func, optional): Function to validate
            the result of the update call. It must have the
            following signature: `validate_result(spec, res)`
            Here, `spec` is the result of the create endpoint
            and `res` is the result of the delete endpoint. In the
            function, use assert to validate the results so that
            invalid data leads to an assertion error.
            If it is unspecified, `spec` and `res` are assumed to be
            of type dict and all `k`,`v` in `spec` are asserted to
            be the same for `res`.
        exception_type (:obj:`Exception`, optional): The exception
            type that is expected to be thrown when calling the
            endpoint with the invalid data. By default, Exception
            is used.
        kwargs
            Additional keyword args are passed to the valids method
            of the component when creating the valid test specs.

    Returns:
        list: List of the valid specs generated and tested.
    """
    valids = component.valids(**{
        **kwargs,
        "endpoint": component.endpoints.create,
    })
    print("TEST DELETE VALIDS:", len(valids))
    for valid in valids:
        print("VALID CREATE SPEC:", valid)
        data = component.endpoints.create.call(valid)
        print("RESULT DATA:", data)
        res = component.endpoints.delete.call(data)
        assert res, "result of delete endpoint None for {}".format(data)
        validate_result(data, res)
        with pytest.raises(exception_type) as e:
            component.endpoints.delete.call(data)
    return valids


def delete_invalids(component, invalids, exception_type=Exception, **kwargs):
    """Test the delete endpoint with valid data.

    For each entry specified in `invalids`, the delete endpoint
    of `component` is called and it is asserted that an exception
    of the specified type is raised.

    Args:
        component (:obj:`Component`)
            The component whose create endpoint to test.
        invalids (list): List of invalid delete specs to be tested.
        exception_type (:obj:`Exception`, optional): The exception
            type that is expected to be thrown when calling the
            endpoint with the invalid data. By default, Exception
            is used.
        kwargs
            Additional keyword args are passed to the valids method
            of the component when creating the valid test specs.

    Returns:
        list: List of the invalid specs tested.
    """
    print("TEST DELETE INVALIDS:", len(invalids))
    for invalid in invalids:
        print("INVALID DELETE SPEC:", invalid)
        with pytest.raises(exception_type) as e:
            component.endpoints.delete.call(invalid)
    return invalids


def list_total(component, total_from_res=None, instance_count=10):
    if total_from_res is None:
        total_from_res = lambda res: len(res)
    current_count = total_from_res(component.endpoints.list.call({}))
    instances = []
    print("TEST LIST TOTAL:", instance_count)
    for i in range(instance_count):
        instances.append(Instance(component).__enter__())
        current_count_ = total_from_res(component.endpoints.list.call({}))
        assert current_count_ == current_count + 1, (current_count_, current_count)
        current_count = current_count_
    for instance in instances:
        instance.__exit__(None, None, None)
        current_count_ = total_from_res(component.endpoints.list.call({}))
        assert current_count_ == current_count - 1, (current_count_, current_count)
        current_count = current_count_


def list_valids(component, total_from_res=None, instance_count=10, **kwargs):
    valids = component.valids(**{
        **kwargs,
        "endpoint": component.endpoints.list,
    })
    instances = []
    print("TEST LIST VALIDS:", instance_count)
    for i in range(instance_count):
        instances.append(Instance(component).__enter__())
    for valid in valids:
        print("VALID LIST SPEC:", valid)
        component.endpoints.list.call(valid)
    for instance in instances:
        instance.__exit__(None, None, None)
    return valids


def list_invalids(component, total_from_res=None, instance_count=10, **kwargs):
    invalids = component.invalids(**{
        **kwargs,
        "endpoint": component.endpoints.list,
        "reason": True,
    })
    instances = []
    print("TEST LIST INVALIDS:", instance_count)
    for i in range(instance_count):
        instances.append(Instance(component).__enter__())
    for invalid,reason in invalids:
        print("INVALID LIST SPEC:", invalid)
        print("           REASON:", reason)
        with pytest.raises(Exception):
            component.endpoints.list.call(invalid)
    for instance in instances:
        instance.__exit__(None, None, None)
    return invalids
