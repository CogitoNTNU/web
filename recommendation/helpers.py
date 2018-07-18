from .models import Entry


def get_entry_tags(entry):
    """
    :param entry: Entry object
    :return: The tags of that object as a list
    """
    return entry.tags[1:-1].replace("'", "").split(",")


def get_related_entries(entry):
    """
    :param entry: Entry object
    :return: list of Entry objects sorted in descending order by the number of tags shared with param entry.
    """
    # Creates a dict with keys=Entry objects, values=no. same tags as param entry
    tags = get_entry_tags(entry)
    entry_tag_dict = {_entry: get_entry_tags(_entry) for _entry in Entry.objects.all()}
    entry_tag_dict.pop(entry)  # removes param entry from list of entries to avoid matching with itself
    for key, value in entry_tag_dict.items():  # switches the values from lists of tags to # tags in common with param
        entry_tag_dict[key] = len(set(tags).intersection(set(value)))

    # creates the list mentioned as :return
    sorted_entry_list = []  # The starting list must contain at least one item
    for key, value in entry_tag_dict.items():
        i = 0
        try:
            while value < entry_tag_dict[sorted_entry_list[i]]:
                i += 1
        except IndexError:
            pass
        finally:
            sorted_entry_list.insert(i, key)

    return sorted_entry_list

