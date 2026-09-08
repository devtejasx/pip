Stop treating a directory that merely shares a name prefix with ``sys.prefix``,
the user site directory or ``site-packages`` as being inside it. A distribution
installed in a sibling environment such as ``env-old`` next to ``env`` was
reported as local and, during uninstall, was permitted to be removed.
