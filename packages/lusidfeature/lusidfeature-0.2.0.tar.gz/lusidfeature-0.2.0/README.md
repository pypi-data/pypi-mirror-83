![LUSID_by_Finbourne](https://content.finbourne.com/LUSID_repo.png)

# Lusid Feature Python Decorator Scanner

## Description

This repository contains source code which provides a python decorator called 'lusid_feature', which can then be used
within a python project to scan through all 'lusid_feature' decorator values in a desired project package. The runner
will then produce an output text file of desired name and path with all lusid_feature codes.

The generated text file is then passed into a Lusid feature reporter python script, which maps the feature codes to 
full feature names and their implementation status, ultimately creating a visual features report across all Lusid SDKs.

## Usage

### Installing

Run:
```
pip install lusidfeature
```

### Importing

This repository has two main functions that need to be imported for the scanner to work

1. lusid_feature in lusid_feature.py - The decorator used with functions and methods
2. extract_features_to_file(argv) in reporter - The function that extracts all decorator values and writes them to a file

### Implementing `lusid_feature` decorator

When successfully imported, lusid_feature decorator can be used to decorate functions and methods in the following manner: 

```
from lusidfeature import lusid_feature

@lusid_feature("F1")
def some_function():
    pass # function/method implementation
```

Rules around using lusid_feature decorator:
- The decorator must always be called with brackets, and have a string value passed. 
Correct Usage: ```@lusid_feature("F1")``` 
Incorrect Usage:```@lusid_feature```
- The decorator must not have an empty string passed. The following will throw an error: 
```@lusid_feature("")```
- The decorator must not have duplicate feature values across the package files that are being scanned. 
The following will throw an error if both functions/methods with the same feature codes are found in the same package:
```
@lusid_feature("F1")
def some_function():
    pass # function/method implementation

@lusid_feature("F1")
def some_other_function():
    pass # function/method implementation
```


### Running the decorator scanner

To extract the feature values and write them to a file, the following function must be imported and run from a main function in a main.py file:

```
from lusidfeature.reporter import extract_features_to_file

def main(argv):
    extract_features_to_file(argv)


if __name__ == "__main__":
    main(sys.argv)

```

The reason we must use 'if __name__ == "__main__"' with an entry main function is because the decorator scanner 
must be run directly, together with strictly required "root project directory", "project package name" 
and "output file path" parameters.


### Input parameters (sys.argv)

The command line requires two parameters

- --outpath or -o <br>
This is the full qualified filename of where to create the output file

Examples:

_Windows_:
```
-o <your-absolute-path>\<your-filename>.txt

-o C:\\home\src\output\features.txt
```

_Unix (Mac/Linux)_:
```
-o <your-absolute-path>/<your-filename>.txt

-o home/src/output/features.txt
```
- --package or -p <br>
This is the package that the decorator scanner should look for decorators in
Examples:
```
-p lusid.submodule
-p lusid.submodule.anothersubmodule
-p tests.tutorials
```

- --root or -r <br>
The path of root directory from which the decorator scanner should start traversing packages and modules. 
The path must point to a directory within the project folder, and not to a directory outside the project. 
(Recommended to be the root SDK folder or src folder rather than the base project path.)

Examples:

_Windows_:
```
-r C:\\home\lusid-sdk-python\sdk
```

_Unix (Mac/Linux)_:
```
-r home/lusid-sdk-python/sdk
```

To run, set your PYTHONPATH for the required folders and run the following example in a similar way:

```
python main.py -p "tests.tutorials" -o "/usr/app/features.txt"
```

## Output file

The decorator scanner should write a file to the specified path with the example content:

features.txt

```
F1
F32
F2
F3
F10
F11
F8
etc...
```
