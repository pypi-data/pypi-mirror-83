# Likelycause2

Likelycause is an utility package that uses several functions to attribute causes to variations. Using a combination of arithmetical decompositions and bayesian techniques, this was built to facilitate the workflow of a data-analyst working for the private sector.

## What the package contains
This package has everything built under the likelycause2 module, so all the functions should be called using “likelycause2.”. Currently, we have 1 auxiliary function and 1 causal function.

### Auxiliary functions
- likelycause2.last_period: The last period function is a utility function that builds variation variables in a dataframe._

### Causal functions
- likelycause2.bayes_suspects: The bayes_suspects function calculates the conditional probabilities of the event and each suspicious causes or a combination of those causes.  It also suggests an attribution to each individual cause, by adjusting the intersections of causes

## Likelycause2.last_period

### Description:
The last period function is a utility function that builds variation variables in a dataframe.
Variations are defined between moment t and a moment in the past.

### Arguments:

- df (pd.DataFrame): the dataframe
- unique_id (string): unique identifier of each line. Must be unique, and can only be 1 column
- interval (string): what is the interval you want to calculate variations for. Accepts days, weeks and hours
- periods (int): number of periods you want to look back on that interval. For last variations, for example, the argument period would be 1
- date_column (string): the date column in your dateframe. Must be a datetime. To convert, use pandas.to_datetime function
- to_past (list): list of columns you want to calculate the variations for

### Returns:
Returns the dataframe that was inputed with additinal columns named v+name of the columns in the to_past argument. Those columns represent the variation of that variable between moment t and t-periods. This variation is calculated as (Variable in moment t)/(Variable in moment t-periods).


## Likelycause2.bayes_suspects

### Description:
The bayes_suspects function calculates the conditional probabilities of the event and each suspicious causes or a combination of those causes. 
It also suggests an attribution to each individual cause, by adjusting the intersections of causes

### Arguments:

- df (pd.DataFrame): the dataframe
- event (string): name of the column that contains the event that we want to explain
- suspects (list): list with name of the columns that contains the potential causes for what we want to explain
- point (dictionary): dictionary with the point for which we want to calculate the probability. Must be a combination of the cause and all the individual points of suspects

### Returns:
Returns a dataframe with all the possible probabilities combinations, and the conditional probabilities:

- name: name of that conditional combination. If it has one event, it represents P(event|a). If it has 2 events it represents P(event1 & event2|a)
- prob_ba: P(cause | event)
- prob_a: P(cause)
- prob_b: P(event)
- pbayes: confitional probability
- pbayes_attribution: suggested probability attribution if we want to attribute to individual causes
