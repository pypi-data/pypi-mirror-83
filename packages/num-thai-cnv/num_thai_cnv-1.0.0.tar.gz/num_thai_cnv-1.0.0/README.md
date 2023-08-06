# num-thai-cnv
num-thai-cnv is python library, primarily focused on converting number into Thai text and vice versa.

# Installation
```sh
pip install GoneJaguar300
```
# Features 
    Convert number to Thai text and vice versa, convert Arabic to Thai number.
    
# Initialize the object
    from GoneJaguar300 import ThaiNumberConverter
    thainum = ThaiNumberConverter()
    
# Number Localization Methods
| Method name | Description |  Command  | Result   |
| ------ | ------ | -------------------- |  ----------- |
| ToText | Convert Arabic number to Thai text |  thainum.ToText(123) or thainum.ToText('123') | 'หนึ่งร้อยยี่สิบสาม'
| ToNum  | Convert Thai text to Arabic number | thainum.ToNum('หนึ่งร้อยยี่สิบสาม') | '123'
| ToThaiNumber | Convert Arabic number to Thai number | thainum(123) or thainum('123') |'๑๒๓'

### Number Localization Notes

- ToText and ToThaiNumber method can support unlimited digit.
- ToNum method will whitelist the following words, violation will lead to error 'Check if text contains excluded word'. 

    | Words |Words  |Words   |
    | ------ | ---- | ------|
    |เอ็ด|หก| ร้อย
    |หนึ่ง|เจ็ด|พัน
    |สอง|แปด  |  หมื่น
    |สาม| เก้า |แสน
    |สี่|สิบ|ล้าน
    |ห้า|ยี่|


