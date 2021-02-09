# coffeeSimulation 

Discrete time simulation for a coffeeshop. 

A coffeeshop has 3 tables, each with 3 different sizes:
Table 1 can accomodate 1 person
Table 2 can accommodate 2 people
Table 3 can accommodate 3 people

This simulation requires past data to run. The `coffee.csv` file contains a small table with past events. 

Considerations
- Profit is calculated as soon as the group sits in the table. 
- This coffeeshop does not allow queueing (possibly it's a tiny location!).
- The customer groups will prefer to sit in the most convenient table according to the size (i.e. if a group of 2 arrives, the group will prefer to sit in table 2). If this table is taken by another group, then the group will sit in the next largest table.
- Special case: If a group of 3 arrives in the coffeeshop and the table for 3 is busy, but the tables for 1 and 2 are available, then this group will join these tables.
- Should there be a clash between an arrival and a service completion for the same table, considering no queueing (or 'waiting') is allowed, the incoming group will not sit.
