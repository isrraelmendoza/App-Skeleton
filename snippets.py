import logging
import argparse
import psycopg2

# Set the log output file and the log level
logging.basicConfig(filename = "snippets.log", level = logging.DEBUG)
logging.debug("Connecting to PostgreSQL")
connection = psycopg2.connect(database="snippets")
logging.debug("Database connection established.")


def put(name, snippet):
    """
    Store a snippet with an associated name.
    Returns the name and the snippet
    """
    logging.info("Storing snippet {!r}: {!r}".format(name, snippet))
    with connection, connection.cursor() as cursor:
        try:
            cursor.execute("INSERT INTO snippets VALUES (%s, %s)", (name, snippet))
        except psycopg2.IntegrityError as e:
            cursor.execute("update snippets set message = %s where keyword = %s", (snippet, name))
    logging.debug("Snippet stored successfully.")
    return name, snippet


def get(name):
    """Retrieve the snippet with a given name.
    If there is no such snippet, return '404: Snippet Not Found'.
    Returns the snippet.
    """
    logging.info("Retrieving snippet {!r}".format(name))
    with connection, connection.cursor() as cursor:
        cursor.execute("select message from snippets where keyword=%s", (name,))
        snippet = cursor.fetchone()  # Have to assign return value to variable
    logging.debug("Snippet retrieved successfully.")
    if not snippet: # No snippet was found with that keyword name
        return "404: Snippet not found"
    else:
        return snippet[0]   # Return only the snippet
        
def catalog():
    """Return a list of keywords available."""
    logging.info("Retrieving keywords")
    with connection, connection.cursor() as cursor:
        cursor.execute("SELECT * FROM snippets ORDER BY keyword")
        rows = cursor.fetchall()    # Returns a list of tuples
    logging.debug("Keywords retrieved successfully")
    names = [x[0] for x in rows]    # Get the first tuple item for each list item
    return names

def search(query):
    """Retrieve list of snippets that contain the search query string.
    Returns a list.
    """

    logging.info("Retrieving search query")
    query = "'%" + query + "%'"
    with connection, connection.cursor() as cursor:
        cursor.execute("SELECT * FROM snippets WHERE message LIKE %s" %(query,))
        queries = cursor.fetchall()
    logging.debug("Search query finished successfully")
    return queries    
    
def main():
    """Main function"""
    logging.info("Constructing parser")
    parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Subparser for the put command
    logging.debug("Constructing put subparser")
    put_parser = subparsers.add_parser("put", help="Store a snippet")
    put_parser.add_argument("name", help="Name of the snippet")
    put_parser.add_argument("snippet", help="Snippet text")

    # Subparser for get command
    logging.debug("Constructing get subparser")
    get_parser = subparsers.add_parser("get", help = "Return a snippet")
    get_parser.add_argument("name", help = "Name of the snippet")
    
    # Subparser for catalog command
    logging.debug("Constructing catalog subparser")
    catalog_parser = subparsers.add_parser("catalog", help = "Return all keywords")

     # Subparser for search command
    logging.debug("Constructing search subparser")
    search_parser = subparsers.add_parser("search", help = "Return snippets with given string")
    search_parser.add_argument("query", help = "String to search for")



    arguments = parser.parse_args()
    # Convert parsed arguments from Namespace to dictionary
    arguments = vars(arguments)
    command = arguments.pop("command")

    if command == "put":
        name, snippet = put(**arguments)
        print("Stored {!r} as {!r}".format(snippet, name))
    elif command == "get":
        snippet = get(**arguments)
        print("Retrieved snippet: {!r}".format(snippet))
    elif command == "catalog":
        keywords = catalog()
        print ("Keywords: {!r}".format(keywords))
    elif command == "search":
        entries = search(**arguments)
        print ("Snippets that contain your query: {!r}".format(entries))

if __name__ == "__main__":
    main()
    
