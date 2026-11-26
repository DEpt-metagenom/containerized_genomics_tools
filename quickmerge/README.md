# docker-quickmerge

Docker image containing Quickmerge with unreleased commits included to support MUMMer4 which supports multi-threading. MUMMer 4.0.1 is also installed in the container instead of MUMMer 3.23 for this reason.

Usage: `merge_wrapper.py -v -t [threads] -l [cutoff] [assembly1] [assembly2]`

`-v` tells Quickmerge to use MUMMer4, `-l` is typically 0.
