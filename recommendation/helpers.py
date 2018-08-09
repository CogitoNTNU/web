from .models import Entry


def get_related_entries(entry):
    """
    :param entry: Entry object
    :return: list of Entry objects sorted in descending order by the number of tags shared with param entry.
    """
    # Creates a dict with keys=Entry objects, values=no. same tags as param entry
    tags = entry.tags.all()
    entry_tag_dict = {_entry: _entry.tags.all() for _entry in Entry.objects.all()}
    entry_tag_dict.pop(entry)  # removes param entry from list of entries to avoid matching with itself
    for key, value in entry_tag_dict.items():
        entry_tag_dict[key] = len(set(tags).intersection(set(value)))

    # creates the list mentioned as :return
    sorted_entry_list = []
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


