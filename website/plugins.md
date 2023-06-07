# Writing plugins for SimpleMediaUpscalerLite

Your plugin has to fulfill the following requirements:
- Name of class it exposes has to be [name of engine]Scaler. The name of the file should be just the name of the engine in all lower case.
- It has to support a folder or an individual file as an input and the function, has to take the following arguments:

Argument | Variable type 
---------|---------------
x        | y

- The function has to return the path to the folder where the final resulting images are located.