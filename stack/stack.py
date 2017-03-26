import persisted

from datetime import datetime

class Stack(object):
    """ A stack of pages a user has saved for later viewing. """

    title_key = "title"
    """ as_sorted_list[index][title_key]: the page's title """

    timestamp_key = "timestamp"
    """ as_sorted_list[index][timestamp_key]: the timestamp for the page """

    url_key = "url"
    """ as_sorted_list[index][url_key]: the URL to the page """

    def __init__(self, backing_file):
        """ Initializes a new stack using the provided file. """
        self.pages = persisted.Map(backing_file)

    def add(self, url, title, timestamp):
        """ Adds a new page to the stack.

        Args:
            url (str)
                The URL of the new item.
            title (str)
                The title of the page.
            timestamp (float)
                The time in seconds since the UNIX epoch.

        """
        # Adding the URL to the page dictionary is redundant. However, in the
        # as_sorted_list method, we want to return a representation of the stack
        # as a list of dictionaries. So we add the URL to the page dictionary
        # here to simplify that logic.
        page = {
            self.title_key : title,
            self.timestamp_key : timestamp,
            self.url_key : url
        }
        self.pages[url] = page

    def delete(self, url):
        """ Deletes a page, referenced by the input URL.

        Args:
            url (str)
                The URL of the page to delete.

        """
        try:
            del self.pages[url]
        except KeyError:
            # If the key doesn't exist, we'll just no-op.
            pass

    def as_sorted_list(self):
        """ Returns the items in this stack, sorted by timestamp.

        Returns:
            sorted_list (dict list)
                The items in this stack, sorted by timestamp. The most recent
                item will be first. Each item is represented as a dictionary.
        """
        # First convert pages to a list of dictionaries.
        pages_list = list(self.pages.itervalues())
        get_timestamp = lambda page: page[self.timestamp_key]
        return sorted(pages_list, key = get_timestamp, reverse=True)

    def __eq__(self, other):
        """ Equality check. Returns NotImplemented for subclasses.

        Args:
            other (Stack)
                Another stack to run an equality check against.

        Returns:
            stacks_equal (bool)
                True iff the input stack is equal to this one. Returns
                NotImplemented if the input stack is a subclass of Stack.

        """
        if type(other) != type(self):
            if isinstance(other, Stack):
                return NotImplemented
            return False
        return self.pages == other.pages

    def __ne__(self, other):
        """ Inequality check. Returns NotImplemented for subclasses.

        Args:
            other (Stack)
                Another stack to run an inequality check against.

        Returns:
            stacks_equal (bool)
                True iff the input stack is not equal to this one. Returns
                NotImplemented if the input stack is a subclass of Stack.

        """
        if type(other) != type(self):
            if isinstance(other, Stack):
                return NotImplemented
            return True
        return self.pages != other.pages
