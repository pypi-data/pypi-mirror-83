This repo hosts 3 useful decorators that might come handy while prototyping namely - 

`@debug`
`@timer`
`@safe_run`

`debug` and `timer` are taken from [https://realpython.com/primer-on-python-decorators/](realpython).

@debug prints the function name with the arguments passed and the return value at the end each time a function is called.

@timer as the name suggests times the function to be executed and in the end prints the total time taken by that function.

`@safe_run` is in brief tries to run the function and prints the error in case the function throws some error. `@safe_run` takes dictionary of parameters also to let the user customize the behavior of it.


