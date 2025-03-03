Here are thoughts, doubts and insights about this whole problem.
A journal to unburden, construct ideas and note realizations.

02/03/2025
----------
After all this time I have finally found out how the jnjn actually works.
I was struggling to understand how the keys from different
tables wouldnt overlap during build, generating inconsistencies and collisions.
The key of it relays on the separation between Ingress and Egress stages.
On the ingress stage, the hash tables are intended to be reserved for build
on table 1, and egress stage contains the build on table 2.

In my head, they needed some kind of identification so you could know which
table inputed the value on a given index. Maybe another hash table only to store
the ids of the table, that corresponds to the index in the table where the join
keys are stored.
Similar to a hash table of tuples (table_id, data), indexed by crc16(data).
This kind of construction is unnecessary in this scenario, given the separation
cited before. Although it `could be useful for joins that involve 3 or more
build stages`. Just and idea for the future.
