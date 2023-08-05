# PIC - pythonImageConverter
A lightweight and easy to use image type converter. Built in Python as a deliverable for my Capstone project.

## Installation

```powershell
pip install pythonImageConverter
```

## Usage

#### For single pictures:

```powershell
pic [input file name] [output file name]
```

#### For entire directories:

```powershell
pic [directory name] [output file type]
```

## Examples

#### Single Files

```powershell
pic test.png test.jpg
```

#### Directories

```powershell
pic ./ png
```

## Supported Image types

  * BMP
  * DIB
  * EPS
  * ICNS
  * ICO
  * IM
  * JPEG
  * JPEG 2000
  * MSP
  * PCX
  * PNG
  * PPM
  * SGI
  * TGA
  * XBM
  
## Todo

* add support for inner folders
* add support for ignoring certain file types
* finish GUI 
