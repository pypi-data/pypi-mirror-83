# yaml-include

## Install
Simply install this tool using pip :

`pip install yaml-include`

## Features :

* Include document using `!include <PATH>`
* Recursive inclusion
* Relative & absolute path

## Usage

Given those three files :

**root.yaml**
```yaml
- Document :
    !include version.yaml

- Job :
    !include jobs/job1.yaml
```

**version.yaml**
```yaml
- name : "4.19.35"
- sha1 : "37dadf3"
```

**jobs/job1.yaml**
```yaml
- name: "Test"
- target: "imx8mq"
```

You can generate your file with included documents using :

`yaml-include root.yaml --output-file generated.yaml`

or simply print the result :

`yaml-include root.yaml`

Resulting this output :

```yaml
- Document:
  - name: 4.19.35
  - sha1: 37dadf3
- Job:
  - name: Test
  - target: imx8mq

```

### Help

```
usage: yaml-include [-h] [-o OUTPUT_FILE] root_document

positional arguments:
  root_document         Root document

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        Path for your generated file.
```