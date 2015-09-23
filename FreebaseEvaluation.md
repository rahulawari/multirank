## Introduction ##

Evaluation of the MultiRank technique using publicly available Freebase data dumps.

## Relationships used ##

Possible "constructive" relationships to use (note: not yet known whether all of these exist):
  * domain created by user
  * topic created by user
  * type created by user (in a domain)
  * type applied to a topic by a user
  * user creates a property (attached to a type)
  * user applies or updates a "datatype" property
  * user applies or updates an "object" property
  * user adds a type to a domain
  * user edits a topic
  * user posts to a discussion on a topic
  * user marks two topics for merge
  * user starts a new thread
  * user adds an article
  * user votes...
  * user flags a topic for...

Possible "destructive" relationships to use:
  * user deletes a topic
  * user deletes a type
  * user un-applies a type to a topic
  * user deletes a property
  * user un-applies a "datatype" property
  * user un-applies an "object" property
  * user removes a type from a domain

Note: there appear to be no special "schema" relationships (a schema is just the collection of properties attached to a type)