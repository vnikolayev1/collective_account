# m_task by Vnikolayev

Create a new module for Odoo v14.

Dependencies: contacts, sale_management.

Assume we have a Sale Order and an Invoice in state DRAFT.

The task consists of several points:
- 1.Create a new model, corresponding XML views, and menuitem.The name of a model is`{module_name}.collective_account`.
  
Table representing a model should contain the following data:
  - a.Product name 
  - b.Total Product QTY
  - c.Total Product Price
  - d.Partner ID
    
So, it should contain GROUPED BY PARTNER AND PRODUCT Invoice data.
- 2.When pressing an Invoice CONFIRM button, the data from each Invoice Line, 
  whichcontains a CONSUMABLE product (without taxes, service products, etc.), 
  should be inserted into the Collective Account table. If a partner already 
  bought some product earlier - update the corresponding record and add QTY and price.
- 3.Create a test case to check the logic.
  
Basic example:

Invoice 1 for Partner 1:
- Product 1, subtotal price 10, QTY 1
  
Invoice 2 for Partner 1:
- Product 1, subtotal price 20, QTY 2
  
Invoice 3 for Partner 2:
- Product 1, subtotal price 40, QTY 4
  
Collective account:
- Product 1, Total QTY 3, Price 30, Partner 1 
- Product 1, Total QTY 4, Price 40, Partner 2
