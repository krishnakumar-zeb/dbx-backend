## Here we are going to clone the presidio repository and analyse what it provides, how it does what it is built for. We are going to deep dive into in by analyzing its components one by one.

## AIM:
I am building a PII Detection and handling project where it takes inputs from different forms of content and performs the masking of the PII entities given.

## Current Scpoe:
The project is in the first phase where we are going with a POC version that takes the text input and does the PII detection and masking of the provided enities:

### Entities:
1.Name
2.Phone Number
3.Government IDs
4.Account Numbers
5.Age
6.Gender
7.Ethnicity
8.City
9.State
10.Zip/Postal Code
11.Email Address
12.IP Address
13.Cookies
14.Certificate Numbers/License Numbers.


## Available Entities from presidio:
1.PERSON
2.PHONE_NUMBER
3.US_SSN
4.US_BANK_NUMBER
5.LOCATION
6.EMAIL_ADDRESS
7.IP_ADDRESS (Only Ipv4)

## Steps for the POC:
We are primarily going to find out how the existing entities work (what each of them use regex/pattern matching/deny list/context based?).
Then we add our custom entities then test it out with sample text that I will provide.
I have the regex pattern matching for the ZIP CODE and the IPV4 and IPV6 regex pattern to use.

