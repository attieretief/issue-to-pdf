# Technical Specification

## Requirement

Standard ProduceLinc functionality applies the Salesperson Code used in Pallet Lines and subsequent Produce Trades, from the Produce Trade Defaults table, if any defaults exist, otherwise from the mapping used in the User Setup table. 

Mapping a salesperson code in the User Setup table is mandatory within standard ProduceLinc. The Produce Trade Default table is designed to store a default salesperson code per customer per commodity group code. 

For scenarios where a single salesperson needs to be associated with a customer, irrespective of the commodity group, the Salesperson Code ought to be derived purely from the Allocated Customer master.

## Justification

Not having the ability to apply the salesperson code from the allocated customer master will require unneccessary and duplicate master data setup to maintain the Produce Trade Default table for each Customer and Commodity Group combination. 

This will require more time and could introduce unnecessary errors and disruptions in the sales allocation process.

## Design

In order to support multiple setup scenarios across the ProduceLinc client base, it is suggested that default Salesperson Codes can be setup in any of the following records:

- User Setup
- Customer master
- Produce Trade Defaults

![image](https://github.com/user-attachments/assets/4972d8b3-cc6c-47c2-a63f-2a55f2a31b22)

### During pallet allocation/redirection, the default Salesperson Code will be applied as follows:

- If a default Salesperson Code mapping exists on the User Setup record for the user performing the allocation/redirection (including import from Excel), then apply that Salesperson Code, else apply nothing and DO NOT generate a error (as is currently the case)
- If a default Salesperson Code mapping exists on the Customer record (allocated customer or redirect customer), then apply that Salesperson Code, else apply nothing. This implies that it will override the previously applied Salesperson Code from the User Setup, if in fact there was anything mapped
- If a default Salesperson Code mapping exists on the relevant Produce Trade Default record (allocated customer or redirect customer and commodity group code), then apply that Salesperson Code, else apply nothing. This implies that it will override the previously applied Salesperson Code from the Customer master, if in fact there was anything mapped
- The allocation or redirection will only be allowed if at least ONE of the above records have a mapped default Salesperson Code

## Acceptance

In the absence of Salesperson Code mappings in either User Setup or Produce Trade Defaults, Salesperson Codes should default from the Customer master during pallet allocation and/or pallet redirection.

# This is another chapter

## This is another page

## And this is yet another page
