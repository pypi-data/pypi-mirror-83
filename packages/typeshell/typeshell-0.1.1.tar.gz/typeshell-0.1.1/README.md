# typeshell-cli

## Description
typeshell-cli is a Python command-line-interface tool that was written as a proof-of-concept of [pytyper](https://github.com/greysonDEV/pytyper), a Python typing test package.

## Installation
```
pip install typeshell
```

## Usage

#### Basic Usage
```
typeshell [-h] [-V] [-v] create count {proverbs, shakespeare}
```

#### Positional Arguments
```
create                 create typing session
count                  number of prompts in session
{proverbs, shakespeare}
                       type of prompts in session
```

#### Optional Arguments
```
-h, --help             show this help message and exit
-V, --version          show program version
-v, --verbose          increase output verbosity
```

#### Examples

To create a typing session with 3 proverbs:
```
typeshell create 3 proverbs
```

A confirmation input is needed before the typing session begins:
```
*-------[Generating session]-------*
              Prompts:              
                 3                  
               Type:                
              proverbs              
*------[Press enter to begin]------*
```

When the session begins, the shell window will be cleared, only displaying the prompt and space for an input:

```
Grief divided is made lighter.

```

Be aware, the timer starts immediately after pressing enter. To exit the current session, stop the shell processes via `KeyboardInterrupt`.

#### Output

Upon finishing a session, the average statistics for that session will be visible:
```
*-------[Finished session]-------*
Average statistics:

Gross-WPM: 71.978
Net-WPM  : 58.446
Accuracy : 0.95
Errors   : 2.334
Time     : 8.102
*----------------------------------*
```

Specifying `--verbose` when creating a typing session will provide an output of each prompt with the user's input, along with an additional line which indicates the errors in the user's input.
```
> Grief divided is made lighter.
$ Grief divided is made lighter.
                                
> A ship in the harbor is safe, but that is not what a ship is for.
$ A ship in the harbor is safe, hut that is not what a ship is for
                                ^                                 ^
> Every man is the architect of his destiny.
$ Ebery man is the architext of his deinrny.
   ^                      ^           ^^^  
```

## License
typeshell is licensed under the [MIT](https://github.com/greysonDEV/typeshell-cli/blob/main/LICENSE) License.


