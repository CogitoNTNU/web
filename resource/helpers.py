from .models import Resource


def get_related_resources(resource, n=-1):
    """
    :param resource: Resource object
    :return: list of Resource objects sorted in descending order by the number of tags shared with param resource.
    """
    # Creates a dict with keys=Resource objects, values=no. same tags as param resource
    tags = resource.tags.all()
    resource_tag_dict = {_resource: _resource.tags.all() for _resource in Resource.objects.all()}
    resource_tag_dict.pop(resource)  # removes param resource from list of resources to avoid matching with itself
    for key, value in resource_tag_dict.items():
        resource_tag_dict[key] = len(set(tags).intersection(set(value)))

    # creates the list mentioned as :return
    sorted_resource_list = []
    for key, value in resource_tag_dict.items():
        i = 0
        try:
            while value < resource_tag_dict[sorted_resource_list[i]]:
                i += 1
        except IndexError:
            pass
        finally:
            sorted_resource_list.insert(i, key)
        if i >= n >= 0:
            break

    return sorted_resource_list


