import pdb

from odoo.addons.base_rest.components.service import to_bool, to_int
from odoo.addons.component.core import Component
from datetime import datetime


class InvoiceService(Component):
    _inherit = "base.rest.service"
    _name = "invoice.service"
    _usage = "invoice"
    _collection = "nutech.services"
    _description = """
        Invoice Services
    """

    def get(self, _id):
        return self._to_json(self._get(_id))
     
    def inquiry(self, **params):
        """
            Inquiry an Order
        """
        data = {
            'response_Code': '02'
        }
        
        invoice = self.env["odoocms.application"].sudo().search([('voucher_number', '=', params['consumer_number'])])
        if invoice:
            inv_date = invoice.expiry_date
            if invoice.fee_voucher_state in ('paid','verify') or invoice.voucher_date:
                data = {
                    'response_Code': '00',
                    'consumer_Detail': invoice.name,
                    'bill_status': 'P',
                    'due_date': inv_date.strftime("%Y%m%d"),
                    'amount_within_dueDate': '+' + (str(int(invoice.amount)) + "00").zfill(13),
                    'amount_after_dueDate': '+' + (str(int(invoice.amount)) + "00").zfill(13),
                    'billing_month': inv_date.strftime("%y%m"),
                    'date_paid': ' ',
                    'amount_paid': ' ',
                    'tran_auth_Id': ' ',
                    'reserved': ''
                }
                return data
            
            data = {
                'response_Code': '00',
                'consumer_Detail': invoice.name,
                'bill_status': 'U',
                'due_date': inv_date.strftime("%Y%m%d"),
                'amount_within_dueDate': '+' + (str(int(invoice.amount)) + "00").zfill(13),
                'amount_after_dueDate': '+' + (str(int(invoice.amount)) + "00").zfill(13),
                'billing_month': inv_date.strftime("%y%m"),
                'date_paid': ' ',
                'amount_paid': ' ',
                'tran_auth_Id': ' ',
                'reserved': ''
            }
            return data
        else:
            data = {
                'response_Code': '01',
            }
        return data
        
        
    def payment(self, **params):
        """
            Update an Order
        """
        invoice = self.env["odoocms.application"].sudo().search([('voucher_number', '=', params['consumer_number'])])
        tran_auth_id = self.env["odoocms.application"].sudo().search([('tran_auth_id', '=', params['tran_auth_id'])])
        
        if invoice and invoice.paid_date:
            data = {
                'response_Code': '04',
                'identification_parameter': params['consumer_number'],
                'reserved': ' '
            }
            return data
        elif tran_auth_id:
            data = {
                'response_Code': '03',
                'identification_parameter': params['consumer_number'],
                'reserved': ' '
            }
            return data
        elif invoice:
            order_data = {
                'paid_amount': int(params['transaction_amount'])/100,
                'paid_date': params['tran_date'],
                'paid_time': params['tran_time'],
                'tran_auth_id': params['tran_auth_id'],
            }
            invoice.sudo().write(order_data)
            data = {
                'response_Code': '00',
                'identification_parameter': params['consumer_number'],
                'reserved': ' '
            }
            return data

        data = {
            'response_Code': '01',
            'identification_parameter': params['consumer_number'],
            'reserved': ' '
        }
        return data

    def _get(self, _id):
        return self.env["nrlp"].sudo().browse(_id)
   
    def _validator_return_get(self):
        res = self._validator_create()
        res.update({"id": {"type": "integer", "required": True, "empty": False}})
        return res

        
    def _validator_payment(self):
        return {
            "consumer_number": {"type": "string", "required": True, "empty": False},
            "tran_auth_id": {"type": "string", "required": True, "empty": False},
            "transaction_amount": {"type": "string", "required": True, "empty": False},
            "tran_date": {"type": "string", "required": True, "empty": False},
            "tran_time": {"type": "string", "required": True, "empty": False},
            # "bank_mnemonic": {"type": "string", "required": True, "empty": False},
            # "reserved": {"type": "string", "nullable": False},
        }
    
    def _validator_return_payment(self):
        res = {
            "response_Code": {"type": "string", "nullable": True},
            "identification_parameter": {"type": "string", "nullable": True},
            "reserved": {"type": "string", "nullable": True},
        }
        return res
    
        # return {
        #     "count": {"type": "integer", "required": True},
        #     "rows": {
        #         "type": "list",
        #         "required": True,
        #         "schema": {"type": "dict", "schema": self._validator_return_get()},
        #     },
        # }
        
    def _validator_create(self):
        res = {
            "consumer_number": {"type": "string", "required": True, "empty": False},
            "customer_name": {"type": "string", "required": True, "empty": False},
            "amount": {"type": "float", "nullable": False},
        }
        return res
    
    def _validator_return_create(self):
        return self._validator_return_get()
    
    def _validator_inquiry(self):
        res = {
            "consumer_number": {"type": "string", "required": True, "empty": False},
            # "bank_mnemonic": {"type": "string", "required": True, "empty": False},
            # "reserved": {"type": "string", "nullable": False},
        }
        return res
    
    def _validator_return_inquiry(self):
        res = {
            "response_Code": {"type": "string", "nullable": True},
            "consumer_Detail": {"type": "string", "nullable": True},
            "bill_status": {"type": "string", "nullable": True},
            "due_date": {"type": "string", "nullable": True},
            "amount_within_dueDate": {"type": "string", "nullable": True},
            "amount_after_dueDate": {"type": "string", "nullable": True},
            "billing_month": {"type": "string", "nullable": True},
            "date_paid": {"type": "string", "nullable": True},
            "amount_paid": {"type": "string", "nullable": True},
            "tran_auth_Id": {"type": "string", "nullable": True},
            "reserved": {"type": "string", "nullable": True},
        }
        return res
    
    def _to_json(self, order):
        res = {
            "id": order.id,
            "consumer_number": order.consumer_number,
            "customer_name": order.customer_name,
            "amount": order.amount,
        }
        return res
