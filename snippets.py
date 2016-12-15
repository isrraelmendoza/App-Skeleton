import logging 
import argparse

#Set the log output file and the log level 
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)

def put(name, snippet):
    """ 
    Store a snippet with an associated name.DEBUG
    
    Returns the name and the snippet
    """
    logging.error("FIXME: Unimplemented - put({!r}, {!r})".format(name, snippet))
    return name, snippet

def get(name):
    """Retrieve the snippet with a given name. 
    
    If there is no such snippet, return '404: Snippet Not Found'.
    
    Returns the snippet.Returns
    """
    logging.error("FIXME: Unimplemented - get({!r})".format(name))
    return ""
    
def main():
    """Main function"""
    logging.info("Constructing parser")
    parser = argpase.ArgumentParser(description="Store and retrieve snippets of text")
    arguments = parser.parse_args()

if __name__ == "main":
    main()