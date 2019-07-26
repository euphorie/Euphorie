# List of things to be resolved before merging this PR

We now have a properly traversable object that can be used to fetch stuff in a more standard way

- check if we can remove the initial_view parameter
- completely remove the SessionManager
- remove wrom the webhelpers the methods that deal with the session (use a survey session view on the context of the traverser to do that)
- clean up the aside-navigator in shell.pt
