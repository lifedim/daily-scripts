/* lookup.i */
%module lookup
%{
/* Put header files here or function declarations like below */
extern char *lookup(char *file_prefix, long file_size, long wc, char *word);
%}

extern char *lookup(char *file_prefix, long file_size, long wc, char *word);
