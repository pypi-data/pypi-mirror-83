# typelint

`typelint` is a program that detects and reports typehints in
Python source code.

List type hints:

    python -m typelint mypython.py

Quiet mode (number is reported as `$?`):

    python -m typelint --quiet mypython.py

In either mode the number of typehints found is reported as the
program's exit status.
Counts above 99 are reported as 99
(so as to avoid overflowing the exit status value,
and to leave some room for reporting errors).

## Exit status

Because the count is reported at the exit status and
the shell's convention is to treat 0 as true (success),
it is convenient to use `typelint` as a test in shell scripts:

    if python typelint.py mypython.py
    then
        echo "no typehints found"
    else
        echo "typehints found"
    fi

## END
