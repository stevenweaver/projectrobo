# Introduction #

We'll use xml
compass information is in degrees

flex information is based on voltage information


| **Flex** | **standing up** | **something bad is happening** |**emergency** | **OMG WTF we're dead** |
|:---------|:----------------|:-------------------------------|:-------------|:-----------------------|
| 1 | 653 | <570 | <500 | <450 |
| 2 | 603 | <530 | <450 | <400 |



ultrasonic is in inches


# Details #

### From Arduino ###
```

<sensor>
  <gps>rawdata</gps>
  <compass>degree</compass>
  <flex>
    <left></left>
    <right></right>
  </flex>
  <ultrasonic>
    <left></left>
    <right></right>
  </ultrasonic>
  <beacon>(forward,left,right, NA)</beacon>
  <wheelencoder>???</wheelencoder>
</sensor>

```

### From Arduino 2 ###
```
<?xml version=\"1.0\"?>
<motor>
<cl><r>1000</r><l>1000</l></cl>
<d><r>0</r><l>1</l></d>
</motor>
```
### To Arduino ###

```
  <direction>right,left,forward,reverse</direction>
```