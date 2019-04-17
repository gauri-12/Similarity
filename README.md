# Similarity
Cosine similarity between books

The file similarity.py takes as input data from book.csv. Book.csv contains information about books such as author name, annotation, etc.

For this task, I look at the following columns/features,
·         Annotation
·         Author, and
·         Series
I generate the cosine similarity between 2 books based on the above features. For the annotation, I generate the TF-IDF and remove all the stop words before looking at the similarity.
The final output format looks like the following.
ISBN1  ISBN2  SeriesSimilarity  AuthorSimilarity  AnnotationSimilarity
 
 (in tabular form)
 
There will be two types of output for 100 books
· One CSV file with the above format 
· Direct insert into a MongoDB collection (attached csv file showing the collection inserted into MongoDB)
